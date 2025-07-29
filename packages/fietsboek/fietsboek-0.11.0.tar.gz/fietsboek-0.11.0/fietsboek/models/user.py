"""User models for fietsboek."""

import datetime
import enum
import hashlib
import secrets
import uuid
from functools import reduce
from typing import TYPE_CHECKING, Optional

from cryptography.exceptions import InvalidKey
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from pyramid.authorization import ALL_PERMISSIONS, Allow
from pyramid.httpexceptions import HTTPNotFound
from pyramid.request import Request
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    LargeBinary,
    Table,
    Text,
    UniqueConstraint,
    delete,
    func,
    select,
    union,
)
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Mapped, Session, relationship, with_parent
from sqlalchemy.orm.attributes import flag_dirty
from sqlalchemy.orm.session import object_session

from .meta import Base

if TYPE_CHECKING:
    from .comment import Comment
    from .track import Track, Upload


class PasswordMismatch(Exception):
    """Exception that is raised if the passwords mismatch.

    Using an exception forces the handling of the password mismatch and makes
    it impossible to accidentally ignore the return value of the password
    verification.
    """


# The parameters were chosen according to the documentation in
# https://cryptography.io/en/latest/hazmat/primitives/key-derivation-functions/#cryptography.hazmat.primitives.kdf.scrypt.Scrypt
SCRYPT_PARAMETERS = {
    "length": 32,
    "n": 2**14,
    "r": 8,
    "p": 1,
}
SALT_LENGTH = 32
SESSION_SECRET_LENGTH = 32
"""Length of the secret bytes for the user's session."""

TOKEN_LIFETIME = datetime.timedelta(hours=24)
"""Maximum validity time of a token."""

FINGERPRINT_SHAKE_BYTES = 10
"""Number of bytes to include in the SHAKE digest of the fingerprint."""


friends_assoc = Table(
    "friends_assoc",
    Base.metadata,
    Column("user_1_id", ForeignKey("users.id"), primary_key=True),
    Column("user_2_id", ForeignKey("users.id"), primary_key=True),
)


class User(Base):
    """A fietsboek user.

    :ivar id: Database ID.
    :vartype id: int
    :ivar name: Name of the user.
    :vartype name: str
    :ivar password: (Hashed) Password of the user. Note that you should use
        :meth:`set_password` and :meth:`check_password` to interface with the
        password instead of accessing this field directly.
    :vartype password: bytes
    :ivar salt: Password salt.
    :vartype salt: bytes
    :ivar email: Email address of the user.
    :vartype email: str
    :ivar session_secret: Secret bytes for the session fingerprint.
    :vartype session_secret: bytes
    :ivar is_admin: Flag determining whether this user has admin access.
    :vartype is_admin: bool
    :ivar is_verified: Flag determining whether this user has been verified.
    :vartype is_verified: bool
    :ivar tracks: Tracks owned by this user.
    :vartype tracks: list[fietsboek.models.track.Track]
    :ivar tagged_tracks: Tracks in which this user is tagged.
    :vartype tagged_tracks: list[fietsboek.models.track.Track]
    :ivar uploads: Currently ongoing uploads by this user.
    :vartype uploads: list[fietsboek.models.track.Upload]
    :ivar tokens: List of tokens that this user can use.
    :vartype tokens: list[fietsboek.models.user.Token]
    :ivar comments: List of comments left by this user.
    :vartype comments: list[fietsboek.model.comment.Comment]
    """

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    password = Column(LargeBinary)
    salt = Column(LargeBinary)
    email = Column(Text)
    session_secret = Column(LargeBinary(SESSION_SECRET_LENGTH))
    is_admin = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)

    tracks: Mapped[list["Track"]] = relationship(
        "Track", back_populates="owner", cascade="all, delete-orphan"
    )
    tagged_tracks: Mapped[list["Track"]] = relationship(
        "Track", secondary="track_people_assoc", back_populates="tagged_people"
    )
    favourite_tracks: Mapped[list["Track"]] = relationship(
        "Track", secondary="track_favourite_assoc", back_populates="favourees"
    )
    uploads: Mapped[list["Upload"]] = relationship(
        "Upload", back_populates="owner", cascade="all, delete-orphan"
    )
    tokens: Mapped[list["Token"]] = relationship(
        "Token", back_populates="user", cascade="all, delete-orphan"
    )
    comments: Mapped[list["Comment"]] = relationship(
        "Comment", back_populates="author", cascade="all, delete-orphan"
    )

    # We don't use them, but include them to ensure our cascading works
    friends_1: Mapped[list["User"]] = relationship(
        "User",
        secondary="friends_assoc",
        back_populates="friends_2",
        foreign_keys=[friends_assoc.c.user_1_id],
    )
    friends_2: Mapped[list["User"]] = relationship(
        "User",
        secondary="friends_assoc",
        back_populates="friends_1",
        foreign_keys=[friends_assoc.c.user_2_id],
    )

    @classmethod
    def query_by_email(cls, email):
        """Returns a query that can be used to query a user by its email.

        This properly ensures that the email is matched case-insensitively.

        :param email: The email address to match.
        :type email: str
        :return: The prepared query.
        :rtype: sqlalchemy.sql.selectable.Select
        """
        return select(cls).filter(func.lower(email) == func.lower(cls.email))

    @classmethod
    def factory(cls, request: Request) -> "User":
        """Factory method to pass to a route definition.

        This factory retrieves the user based on the ``user_id`` matched
        route parameter, and returns the user. If the user is not found,
        ``HTTPNotFound`` is raised.

        :raises pyramid.httpexception.NotFound: If the user is not found.
        :param request: The pyramid request.
        :return: The user.
        """
        user_id = request.matchdict["user_id"]
        query = select(cls).filter_by(id=user_id)
        user = request.dbsession.execute(query).scalar_one_or_none()
        if user is None:
            raise HTTPNotFound()
        return user

    def __acl__(self):
        acl = [
            (Allow, "group:admins", ALL_PERMISSIONS),
            (Allow, f"user:{self.id}", ALL_PERMISSIONS),
        ]
        return acl

    def _fingerprint(self) -> str:
        # We're not interested in hiding the data by all means, we just want a
        # good check to see whether the email of the represented user actually
        # matches with the database entry. Therefore, we use a short SHAKE hash.
        email = self.email or ""
        shaker = hashlib.shake_128()
        shaker.update(email.encode("utf-8"))
        shaker.update(self.password or b"")
        shaker.update(self.session_secret or b"")
        return shaker.hexdigest(FINGERPRINT_SHAKE_BYTES)

    def authenticated_user_id(self) -> str:
        """Returns a string suitable to re-identify this user, e.g. in a cookie
        or session.

        The returned ID contains a "fingerprint" to ensure that the
        re-identified user matches.

        :return: The string used to re-identify this user.
        """
        fingerprint = self._fingerprint()
        return f"{self.id}-{fingerprint}"

    @classmethod
    def get_by_authenticated_user_id(cls, session: Session, user_id: str) -> Optional["User"]:
        """Retrieves a user by their authenticated user ID (as returned by
        :meth:`authenticated_user_id`).

        This method returns ``None`` on any of the following conditions:

        * The user ID is malformed.
        * The user with the given ID was not found.
        * The fingerprint of the ``user_id`` and the database user do not match.

        :param session: The database session which to retrieve the user from.
        :param user_id: The user ID.
        :return: The user, if found.
        """
        try:
            numeric_id, fingerprint = user_id.split("-")
        except ValueError:
            # Malformed ID
            return None
        query = select(cls).filter_by(id=numeric_id)
        try:
            user = session.execute(query).scalar_one()
        except NoResultFound:
            return None
        # pylint: disable=protected-access
        if user._fingerprint() != fingerprint:
            return None
        return user

    def set_password(self, new_password):
        """Sets a new password for the user.

        This function automatically generates a new random salt and updates the
        stored password hash and salt value.

        :param new_password: The new password of the user.
        :type new_password: str
        """
        new_password = new_password.encode("utf-8")
        salt = secrets.token_bytes(SALT_LENGTH)
        scrypt = Scrypt(salt=salt, **SCRYPT_PARAMETERS)
        password = scrypt.derive(new_password)
        self.salt = salt
        self.password = password

    def check_password(self, password):
        """Checks if the given password fits for the user.

        Does nothing if the passwords match, raises an exception otherwise.

        :raises PasswordMismatch: When the password does not match the stored
            one.
        :param password: The password to check.
        :type password: str
        """
        password = password.encode("utf-8")
        scrypt = Scrypt(salt=self.salt or b"", **SCRYPT_PARAMETERS)
        try:
            scrypt.verify(password, self.password or b"")
        except InvalidKey:
            raise PasswordMismatch from None

    def roll_session_secret(self):
        """Rolls a new session secret for the user.

        This function automatically generates the right amount of random bytes
        from a secure source.
        """
        self.session_secret = secrets.token_bytes(SESSION_SECRET_LENGTH)

    def principals(self):
        """Returns all principals that this user fulfills.

        This does not include the ``Everyone`` and ``Authenticated``
        principals, as those have to be checked before accessing the user.

        :return: The seceurity principals that this user fulfills.
        :rtype: list[str]
        """
        principals = [f"user:{self.id}"]
        if self.is_admin:
            principals.append("group:admins")
        return principals

    def all_tracks_query(self):
        """Returns a query that selects all the user's tracks.

        This includes the user's own tracks, as well as any tracks the user has
        been tagged in.

        The returned query can be further modified, however, you need to use
        :func:`sqlalchemy.orm.aliased` to access the correct objects:

        >>> from fietsboek.models.track import Track, TrackType
        >>> from sqlalchemy import select
        >>> from sqlalchemy.orm import aliased
        >>> user = retrieve_user()
        >>> query = user.all_tracks_query()
        >>> query = query.filter(query.c.type == TrackType.ORGANIC)
        >>> query = select(aliased(Track, query))

        :rtype: sqlalchemy.sql.expression.Selectable
        """
        # Late import to avoid cycles
        # pylint: disable=import-outside-toplevel
        from .track import Track

        own = select(Track).where(with_parent(self, User.tracks))
        friends = select(Track).where(with_parent(self, User.tagged_tracks))
        # Create a fresh select so we can apply filter operations
        return union(own, friends).subquery()

    @classmethod
    def visible_tracks_query(cls, user=None):
        """Returns a query that selects all tracks visible to the given user.

        The user might be ``None``, in which case tracks for public users are
        returned.

        The returned query can be further modified, however, you need to use
        :func:`sqlalchemy.orm.aliased` to access the correct objects (see also
        :meth:`all_tracks_query`).

        :param user: The user for which the tracks should be searched.
        :type user: User
        :rtype: sqlalchemy.sql.expression.Selectable
        """
        # Late import to avoid cycles
        # pylint: disable=import-outside-toplevel,protected-access
        from .track import Track, Visibility, track_people_assoc

        # We build the list of visible tracks in multiple steps, and then union
        # them later.
        queries = []
        # Step 1: Own tracks and tagged tracks
        if user:
            queries.append(select(user.all_tracks_query()))
        # Step 2: Public tracks
        queries.append(select(Track).where(Track.visibility == Visibility.PUBLIC))
        # Step 3: Logged in
        if user:
            queries.append(select(Track).where(Track.visibility == Visibility.LOGGED_IN))
        # Step 4: Friends' tracks
        if user:
            friend_query = user._friend_query().subquery()
            friend_ids = select(friend_query.c.id)
            queries.append(
                select(Track)
                # The owner also counts as a "tagged person", so we need to
                # include FRIENDS_TAGGED here as well.
                .where(Track.visibility.in_([Visibility.FRIENDS, Visibility.FRIENDS_TAGGED])).where(
                    Track.owner_id.in_(friend_ids)
                )
            )
        # Step 5: Am I a friend of a tagged person?
        # We do this via a big join:
        # Table -> Tagged people -> Friends (per column 1)
        # Table -> Tagged people -> Friends (per column 2)
        # With those, we have a product that contains a track and all friends
        # that this track should be visible to.
        if user:
            queries.append(
                select(Track)
                .join(track_people_assoc)
                .join(friends_assoc, track_people_assoc.c.user_id == friends_assoc.c.user_1_id)
                .where(friends_assoc.c.user_2_id == user.id)
                .where(Track.visibility == Visibility.FRIENDS_TAGGED)
            )
            queries.append(
                select(Track)
                .join(track_people_assoc)
                .join(friends_assoc, track_people_assoc.c.user_id == friends_assoc.c.user_2_id)
                .where(friends_assoc.c.user_1_id == user.id)
                .where(Track.visibility == Visibility.FRIENDS_TAGGED)
            )

        return union(*queries)

    def _friend_query(self):
        qry1 = select(User).filter(
            friends_assoc.c.user_1_id == self.id, friends_assoc.c.user_2_id == User.id
        )
        qry2 = select(User).filter(
            friends_assoc.c.user_2_id == self.id, friends_assoc.c.user_1_id == User.id
        )
        return union(qry1, qry2)

    def get_friends(self):
        """Returns all friends of the user.

        This is not a simple SQLAlchemy property because the friendship
        relation  is complex.

        :return: All friends of this user.
        :rtype: list[User]
        """
        session = object_session(self)
        assert session
        query = select(User).from_statement(self._friend_query())
        yield from session.execute(query).scalars()

    def remove_friend(self, friend):
        """Remove the friend relationship between two users.

        :param friend: The befriended user.
        :type friend: User
        """
        session = object_session(self)
        assert session
        session.execute(delete(friends_assoc).filter_by(user_1_id=self.id, user_2_id=friend.id))
        session.execute(delete(friends_assoc).filter_by(user_1_id=friend.id, user_2_id=self.id))
        flag_dirty(self)

    def add_friend(self, friend):
        """Add the given user as a new friend.

        :param friend: The user to befriend.
        :type friend: User
        """
        session = object_session(self)
        assert session
        if self.id > friend.id:
            friend.add_friend(self)
            return
        stmt = friends_assoc.insert().values(user_1_id=self.id, user_2_id=friend.id)
        session.execute(stmt)

    def toggle_favourite(self, track: "Track"):
        """Toggles the favourite status for the given track.

        :param track: The track to (un)favour.
        """
        if track in self.favourite_tracks:
            self.favourite_tracks.remove(track)
        else:
            self.favourite_tracks.append(track)

    def autocomplete_tags(self):
        """Returns all tags the user has ever used, suitable for autocompletion
        lists.

        :return: All tags of the user.
        :rtype: ~collections.abc.Iterator[str]
        """
        return reduce(lambda acc, track: acc | track.text_tags(), self.tracks, set())


Index("idx_users_email", User.email, unique=True)


class FriendRequest(Base):
    """Represents a request of friendship between two :class:`User`\\s.

    :ivar id: Database ID.
    :vartype id: int
    :ivar sender_id: ID of the friendship initiator.
    :vartype sender_id: int
    :ivar recipient_id: ID of the request recipient.
    :vartype recipient_id: int
    :ivar date: Date of the request.
    :vartype date: datetime.datetime
    :ivar sender: Initiator of the friendship request.
    :vartype sender: User
    :ivar recipient: Recipient of the friendship.
    :vartype recipient: User
    """

    # pylint: disable=too-few-public-methods
    __tablename__ = "friend_requests"
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    recipient_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime(False))

    sender: Mapped["User"] = relationship(
        "User", primaryjoin="User.id == FriendRequest.sender_id", backref="outgoing_requests"
    )
    recipient: Mapped["User"] = relationship(
        "User", primaryjoin="User.id == FriendRequest.recipient_id", backref="incoming_requests"
    )

    __table_args__ = (UniqueConstraint("sender_id", "recipient_id"),)


class TokenType(enum.Enum):
    """Type of tokens.

    A token can be used either to verify the user's email, or it can be used to
    reset the password.
    """

    VERIFY_EMAIL = enum.auto()
    """A token that can be used to verify a user's email."""
    RESET_PASSWORD = enum.auto()
    """A token that can be used to reset a user's password."""


class Token(Base):
    """A token is something that a user can use to perform certain account
    related functions.

    A token with type :const:`TokenType.VERIFY_EMAIL` can be used by the user to
    verify their email address.

    A token with type :const:`TokenType.RESET_PASSWORD` can be used by the user
    to reset their password.

    :ivar id: Database ID.
    :vartype id: int
    :ivar user_id: ID of the user.
    :vartype user_id: int
    :ivar uuid: The token UUID.
    :vartype uuid: str
    :ivar token_type: The type of the token.
    :vartype token_type: TokenType
    :ivar date: Date of the token creation, in UTC.
    :vartype date: datetime.datetime
    :ivar user: User that this token belongs to.
    :vartype user: User
    """

    # pylint: disable=too-few-public-methods
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    uuid = Column(Text)
    token_type = Column(Enum(TokenType))
    date = Column(DateTime(False))

    user: Mapped["User"] = relationship("User", back_populates="tokens")

    @classmethod
    def generate(cls, user, token_type):
        """Generate a new token for the given user.

        :param user: The user which to generate the token for.
        :type user: User
        :param token_type: The type of the token to generate.
        :type token_type: TokenType
        :return: The generated token.
        :rtype: Token
        """
        token_uuid = str(uuid.uuid4())
        now = datetime.datetime.now(datetime.UTC).replace(tzinfo=None)
        return cls(user=user, uuid=token_uuid, date=now, token_type=token_type)

    def age(self) -> datetime.timedelta:
        """Returns the age of the token."""
        if self.date is None:
            return datetime.timedelta()
        now = datetime.datetime.now(datetime.UTC).replace(tzinfo=None)
        return abs(now - self.date)


Index("idx_token_uuid", Token.uuid, unique=True)


__all__ = [
    "PasswordMismatch",
    "SCRYPT_PARAMETERS",
    "SALT_LENGTH",
    "SESSION_SECRET_LENGTH",
    "TOKEN_LIFETIME",
    "FINGERPRINT_SHAKE_BYTES",
    "friends_assoc",
    "User",
    "FriendRequest",
    "TokenType",
    "Token",
]

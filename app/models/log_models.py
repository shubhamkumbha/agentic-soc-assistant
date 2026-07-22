from sqlalchemy import DateTime, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database.client import Base


class BaseLogModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    document: Mapped[dict] = mapped_column(JSONB)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )


class FTPLog(BaseLogModel):
    __tablename__ = "ftp_logs"


class HTTPSLog(BaseLogModel):
    __tablename__ = "https_logs"


class OctopusLog(BaseLogModel):
    __tablename__ = "octopus_logs"


class RDPLog(BaseLogModel):
    __tablename__ = "rdp_logs"


class SQLILog(BaseLogModel):
    __tablename__ = "sqli_logs"


class SSHLog(BaseLogModel):
    __tablename__ = "ssh_logs"


class BinariesAnalytics(BaseLogModel):
    __tablename__ = "binaries_analytics"
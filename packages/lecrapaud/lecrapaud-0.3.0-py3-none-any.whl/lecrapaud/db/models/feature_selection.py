from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Date,
    Float,
    JSON,
    Table,
    ForeignKey,
    BigInteger,
    Index,
    TIMESTAMP,
    UniqueConstraint,
)
from sqlalchemy import desc, asc, cast, text, func

from sqlalchemy.orm import (
    relationship,
    Mapped,
    mapped_column,
    DeclarativeBase,
    object_session,
)
from collections.abc import Iterable

from lecrapaud.db.session import get_db
from lecrapaud.db.models.base import Base, with_db

# jointures
feature_selection_association = Table(
    "feature_selection_association",
    Base.metadata,
    Column(
        "feature_selection_id",
        BigInteger,
        ForeignKey("feature_selections.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "feature_id",
        BigInteger,
        ForeignKey("features.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class FeatureSelection(Base):
    __tablename__ = "feature_selections"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    training_time = Column(Integer)
    best_features_path = Column(String(255))
    dataset_id = Column(
        BigInteger, ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False
    )
    target_id = Column(
        BigInteger, ForeignKey("targets.id", ondelete="CASCADE"), nullable=False
    )

    dataset = relationship(
        "Dataset", back_populates="feature_selections", lazy="selectin"
    )
    target = relationship(
        "Target", back_populates="feature_selections", lazy="selectin"
    )
    feature_selection_ranks = relationship(
        "FeatureSelectionRank",
        back_populates="feature_selection",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    features = relationship(
        "Feature",
        secondary=feature_selection_association,
        back_populates="feature_selections",
        lazy="selectin",
    )

    __table_args__ = (
        UniqueConstraint(
            "dataset_id", "target_id", name="uq_feature_selection_composite"
        ),
    )

    @with_db
    def add_features(self, features: list, db=None):
        self = db.merge(self)
        for feature in features:
            feature = db.merge(feature)
            if feature not in self.features:
                self.features.append(feature)
        # db.flush()
        # db.refresh(self)
        return self

    @with_db
    def __lshift__(self, feature_or_list, db=None):
        items = (
            feature_or_list
            if isinstance(feature_or_list, Iterable)
            and not isinstance(feature_or_list, (str, bytes))
            else [feature_or_list]
        )

        self = db.merge(self)
        for feature in items:
            feature = db.merge(feature)
            if feature not in self.features:
                self.features.append(feature)

        db.flush()
        db.refresh(self)
        print(self.features)
        return self

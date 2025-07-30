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
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from itertools import chain

from lecrapaud.db.session import get_db
from lecrapaud.db.models.base import Base

# jointures
dataset_target_association = Table(
    "dataset_target_association",
    Base.metadata,
    Column(
        "dataset_id",
        BigInteger,
        ForeignKey("datasets.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "target_id",
        BigInteger,
        ForeignKey("targets.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Dataset(Base):
    __tablename__ = "datasets"

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
    name = Column(String(50), nullable=False)
    path = Column(String(255))  # we do not have this at creation time
    type = Column(String(50), nullable=False)
    size = Column(Integer, nullable=False)
    train_size = Column(Integer)
    val_size = Column(Integer)
    test_size = Column(Integer)
    corr_threshold = Column(Float, nullable=False)
    max_features = Column(Integer, nullable=False)
    percentile = Column(Float, nullable=False)
    number_of_groups = Column(Integer)
    list_of_groups = Column(JSON)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    train_start_date = Column(DateTime)
    train_end_date = Column(DateTime)
    val_start_date = Column(DateTime)
    val_end_date = Column(DateTime)
    test_start_date = Column(DateTime)
    test_end_date = Column(DateTime)

    feature_selections = relationship(
        "FeatureSelection",
        back_populates="dataset",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    model_selections = relationship(
        "ModelSelection",
        back_populates="dataset",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    targets = relationship(
        "Target",
        secondary=dataset_target_association,
        back_populates="datasets",
        lazy="selectin",
    )

    __table_args__ = (
        UniqueConstraint(
            "name",
            name="uq_datasets_composite",
        ),
    )

    def get_features(self, target_number: int):
        feature_selections = self.feature_selections
        target_id = [t for t in self.targets if t.name == f"TARGET_{target_number}"][
            0
        ].id
        feature_selection = [
            fs for fs in feature_selections if fs.target_id == target_id
        ][0]
        feature = [f.name for f in feature_selection.features]
        return feature

    def get_all_features(self, date_column: str = None, group_column: str = None):
        target_idx = [target.id for target in self.targets]
        all_features = []
        if date_column:
            all_features.append(date_column)
        if group_column:
            all_features.append(group_column)
        all_features += list(
            chain.from_iterable(
                [f.name for f in fs.features]
                for fs in self.feature_selections
                if fs.target_id in target_idx
            )
        )
        all_features = list(dict.fromkeys(all_features))

        return all_features

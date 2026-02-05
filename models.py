from datetime import datetime
from sqlalchemy import Column, String, Integer, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    target_country = Column(String(120), nullable=False)
    target_city = Column(String(120), nullable=False)
    clues_json = Column(Text, nullable=False)
    difficulty = Column(String(20), nullable=False, default="easy")
    status = Column(String(20), nullable=False, default="active")
    ai_explanation = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    guesses = relationship("Guess", back_populates="game", cascade="all, delete-orphan")


class Guess(Base):
    __tablename__ = "guesses"

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    guess_text = Column(String(120), nullable=False)
    is_correct = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    game = relationship("Game", back_populates="guesses")

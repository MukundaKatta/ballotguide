"""Tests for Ballotguide."""
from src.core import Ballotguide
def test_init(): assert Ballotguide().get_stats()["ops"] == 0
def test_op(): c = Ballotguide(); c.process(x=1); assert c.get_stats()["ops"] == 1
def test_multi(): c = Ballotguide(); [c.process() for _ in range(5)]; assert c.get_stats()["ops"] == 5
def test_reset(): c = Ballotguide(); c.process(); c.reset(); assert c.get_stats()["ops"] == 0
def test_service_name(): c = Ballotguide(); r = c.process(); assert r["service"] == "ballotguide"

from sqlalchemy import Column, LargeBinary, Numeric, UnicodeText

from julia.modules.sql import BASE, SESSION


class NOTES(BASE):
    __tablename__ = "notes"
    note = Column(UnicodeText, primary_key=True)
    reply = Column(UnicodeText)
    note_type = Column(Numeric)
    media_id = Column(UnicodeText)
    media_access_hash = Column(UnicodeText)
    media_file_reference = Column(LargeBinary)

    def __init__(
        self,
        note,
        reply,
        note_type,
        media_id=None,
        media_access_hash=None,
        media_file_reference=None,
    ):
        self.note = note
        self.reply = reply
        self.note_type = note_type
        self.media_id = media_id
        self.media_access_hash = media_access_hash
        self.media_file_reference = media_file_reference


NOTES.__table__.create(checkfirst=True)


def get_notes(keyword):
    try:
        return SESSION.query(NOTES).get(keyword)
    except:
        return None
    finally:
        SESSION.close()


def get_all_notes():
    try:
        return SESSION.query(NOTES).all()
    except:
        return None
    finally:
        SESSION.close()


def add_note(
    keyword, reply, note_type, media_id, media_access_hash, media_file_reference
):
    adder = SESSION.query(NOTES).get(keyword)
    if adder:
        adder.reply = reply
        adder.note_type = note_type
        adder.media_id = media_id
        adder.media_access_hash = media_access_hash
        adder.media_file_reference = media_file_reference
    else:
        adder = NOTES(
            keyword, reply, note_type, media_id, media_access_hash, media_file_reference
        )
    SESSION.add(adder)
    SESSION.commit()


def remove_note(keyword):
    note = SESSION.query(NOTES).filter(NOTES.note == keyword)
    if note:
        note.delete()
        SESSION.commit()

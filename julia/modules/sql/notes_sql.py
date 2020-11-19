from sqlalchemy import Column, LargeBinary, Numeric, UnicodeText

from julia.modules.sql import BASE, SESSION


class NOTES(BASE):
    __tablename__ = "notes"
    chat_id = Column(String(14), primary_key=True)
    note = Column(UnicodeText, primary_key=True)
    reply = Column(UnicodeText)
    note_type = Column(Numeric)
    media_id = Column(UnicodeText)
    media_access_hash = Column(UnicodeText)
    media_file_reference = Column(LargeBinary)

    def __init__(
        self,
        chat_id,
        note,
        reply,
        note_type,
        media_id=None,
        media_access_hash=None,
        media_file_reference=None,
    ):
        self.chat_id = chat_id
        self.keyword = keyword
        self.note = note
        self.reply = reply
        self.note_type = note_type
        self.media_id = media_id
        self.media_access_hash = media_access_hash
        self.media_file_reference = media_file_reference


NOTES.__table__.create(checkfirst=True)


def get_notes(chat_id, keyword):
    try:
        return SESSION.query(NOTES).get((str(chat_id), keyword))
    except:
        return None
    finally:
        SESSION.close()


def get_all_notes():
    try:
        SESSION.query(NOTES).filter(NOTES.chat_id == str(chat_id)).all()
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


def remove_note(chat_id, keyword):
    saved_note = SESSION.query(NOTES).get((str(chat_id), keyword))
    if saved_note:
        SESSION.delete(saved_note)
        SESSION.commit()

def remove_all_notes(chat_id):
    saved_note = SESSION.query(NOTES).filter(NOTES.chat_id == str(chat_id))
    if saved_note:
        saved_note.delete()
        SESSION.commit()

#!/usr/bin/env python

import unittest
import util


class TestNotes(unittest.TestCase):
    def setUp(self):
        util.invoke('createDeck', deck='test')


    def tearDown(self):
        util.invoke('deleteDecks', decks=['test'], cardsToo=True)


    def runTest(self):
        options = {
            'allowDuplicate': True
        }

        note1 = {
            'deckName': 'test',
            'modelName': 'Basic',
            'fields': {'Front': 'front1', 'Back': 'back1'},
            'tags': ['tag1'],
            'options': options
        }

        note2 = {
            'deckName': 'test',
            'modelName': 'Basic',
            'fields': {'Front': 'front1', 'Back': 'back1'},
            'tags': ['tag1']
        }

        notes1 = [
            {
                'deckName': 'test',
                'modelName': 'Basic',
                'fields': {'Front': 'front3', 'Back': 'back3'},
                'tags': ['tag'],
                'options': options
            },
            {
                'deckName': 'test',
                'modelName': 'Basic',
                'fields': {'Front': 'front4', 'Back': 'back4'},
                'tags': ['tag'],
                'options': options
            }
        ]

        notes2 = [
            {
                'deckName': 'test',
                'modelName': 'Basic',
                'fields': {'Front': 'front3', 'Back': 'back3'},
                'tags': ['tag']
            },
            {
                'deckName': 'test',
                'modelName': 'Basic',
                'fields': {'Front': 'front4', 'Back': 'back4'},
                'tags': ['tag']
            }
        ]


        # addNote
        noteId = util.invoke('addNote', note=note1)
        self.assertRaises(Exception, lambda: util.invoke('addNote', note=note2))

        # addTags
        util.invoke('addTags', notes=[noteId], tags='tag2')

        # notesInfo (part 1)
        noteInfos = util.invoke('notesInfo', notes=[noteId])
        self.assertEqual(len(noteInfos), 1)
        noteInfo = noteInfos[0]
        self.assertEqual(noteInfo['noteId'], noteId)
        self.assertSetEqual(set(noteInfo['tags']), {'tag1', 'tag2'})
        self.assertEqual(noteInfo['fields']['Front']['value'], 'front1')
        self.assertEqual(noteInfo['fields']['Back']['value'], 'back1')

        # getTags
        allTags = util.invoke('getTags')
        self.assertIn('tag1', allTags)
        self.assertIn('tag2', allTags)

        # removeTags
        util.invoke('removeTags', notes=[noteId], tags='tag2')

        # updateNoteFields
        noteUpdate = {'id': noteId, 'fields': {'Front': 'front2', 'Back': 'back2'}}
        util.invoke('updateNoteFields', note=noteUpdate)

        # notesInfo (part 2)
        noteInfos = util.invoke('notesInfo', notes=[noteId])
        self.assertEqual(len(noteInfos), 1)
        noteInfo = noteInfos[0]
        self.assertSetEqual(set(noteInfo['tags']), {'tag1'})
        self.assertIn('tag1', noteInfo['tags'])
        self.assertNotIn('tag2', noteInfo['tags'])
        self.assertEqual(noteInfo['fields']['Front']['value'], 'front2')
        self.assertEqual(noteInfo['fields']['Back']['value'], 'back2')

        # canAddNotes (part 1)
        noteStates = util.invoke('canAddNotes', notes=notes1)
        self.assertEqual(len(noteStates), len(notes1))
        self.assertNotIn(False, noteStates)

        # addNotes (part 1)
        noteIds = util.invoke('addNotes', notes=notes1)
        self.assertEqual(len(noteIds), len(notes1))
        for noteId in noteIds:
            self.assertNotEqual(noteId, None)

        # canAddNotes (part 2)
        noteStates = util.invoke('canAddNotes', notes=notes2)
        self.assertNotIn(True, noteStates)
        self.assertEqual(len(noteStates), len(notes2))

        # addNotes (part 2)
        noteIds = util.invoke('addNotes', notes=notes2)
        self.assertEqual(len(noteIds), len(notes2))
        for noteId in noteIds:
            self.assertEqual(noteId, None)

        # findNotes
        noteIds = util.invoke('findNotes', query='deck:test')
        self.assertEqual(len(noteIds), len(notes1) + 1)

        # deleteNotes
        util.invoke('deleteNotes', notes=noteIds)
        noteIds = util.invoke('findNotes', query='deck:test')
        self.assertEqual(len(noteIds), 0)

if __name__ == '__main__':
    unittest.main()

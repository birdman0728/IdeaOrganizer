"""Simple CLI/demo to exercise MapManager and models for an app.

Run this module to see a short demo of creating maps, documents and tags,
editing/moving items, and listing the final structure.
"""
from map_manager import MapManager


def demo():
    mm = MapManager()

    # create maps
    mm.create_map('Ideas')
    mm.create_map('Inbox')

    # add documents
    d1 = mm.add_document('Ideas', 'Build a tree app', 'Make an app to organize ideas')
    d2 = mm.add_document('Ideas', 'Write blog post', 'Draft for new post')

    # tags
    mm.create_tag('urgent')
    mm.create_tag('writing')
    mm.add_tag_to_document(d1.id, 'urgent')
    mm.add_tag_to_document(d2.id, 'writing')

    # move d2 to Inbox
    mm.move_document(d2.id, 'Ideas', 'Inbox')

    # rename map (creates new map and transfers items)
    mm.rename_map('Ideas', 'Project Ideas')

    # edit document
    mm.edit_document(d1.id, content='Updated plan with milestones')

    print('Maps:', mm.list_maps())
    print('Structure:')
    for m, docs in mm.as_dict().items():
        print(' -', m)
        for doc in docs:
            print('    *', doc['title'], '-', doc['tags'])


if __name__ == '__main__':
    demo()

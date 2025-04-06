python manage.py import_marc21 ems/data/ems_marc_tais.mrc --batch_size 1000
python manage.py transform_tags 
python manage.py import book.models.resources.BookTagResource book/data/book_tag_topic.json --encoding utf8 --format json --no-input
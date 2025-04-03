from django.core.management.base import BaseCommand
from neomodel import db

from book.models import Book
from neom.models import BookNode, PersonNode 


class Command(BaseCommand):
    help = "Migrate Book and related Person models to Neo4j database"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting migration to Neo4j...")

        # Clear existing data in Neo4j
        db.cypher_query("MATCH (n) DETACH DELETE n")
        self.stdout.write("Cleared existing Neo4j data.")

        # Migrate Book and related Person models
        books = Book.objects.all()
        for book in books:
            # Create or get the BookNode
            book_node = BookNode(
                uuid=str(book.uuid),
                title=book.get_label() or "", 
                token=book.token or "",
                published=book.published or "",
            )
            book_node.save()

            # Create or get related PersonNodes and relationships
            for book_person in book.book_persons.filter(relation__name_en="author").all():
                person_node = PersonNode.nodes.first_or_none(
                    uuid=str(book_person.person.uuid),
                    first_name=book_person.person.first_name or "",
                    last_name=book_person.person.last_name or "",
                    birth=book_person.person.birth or "",
                )
                
                if person_node is None:
                    person_node = PersonNode(
                        uuid=str(book_person.person.uuid),
                        first_name=book_person.person.first_name or "",
                        last_name=book_person.person.last_name or "",
                        birth=book_person.person.birth or "",
                    )
                    person_node.save()
                
                book_node.authors.connect(person_node)
                
            # Create or get related PersonNodes and relationships for supervisors
            for book_supervisor in book.book_persons.filter(relation__name_en="supervisor").all():
                supervisor_node = PersonNode.nodes.first_or_none(
                    uuid=str(book_supervisor.person.uuid),
                    first_name=book_supervisor.person.first_name or "",
                    last_name=book_supervisor.person.last_name or "",
                    birth=book_supervisor.person.birth or "",
                )
                
                if supervisor_node is None:
                    supervisor_node = PersonNode(
                        uuid=str(book_supervisor.person.uuid),
                        first_name=book_supervisor.person.first_name or "",
                        last_name=book_supervisor.person.last_name or "",
                        birth=book_supervisor.person.birth or "",
                    )
                    supervisor_node.save()
                
                book_node.supervisors.connect(supervisor_node)

        self.stdout.write("Migration completed successfully.")

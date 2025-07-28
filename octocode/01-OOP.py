class Task :
    def __init__(self, title, director, release_year,genre):
        self.nmu = 0
        self.genre_2 = None
        self.title =title
        self.director=director
        self.release_year=release_year
        self.genre=genre
    def display_task(self):

        print(f"Title: {self.title}")
        print(f"Director: {self.director}")
        print(f"Release Year: {self.release_year}")
        print(f"Genre: {self.genre}\n\n")


    def mark_as_complete(self,directors):


        self.genre_2 = directors
        self.director = self.genre_2

TAsk1=Task("Inception","Christopher Nolan","2010","Sci-Fi")
TAsk2=Task("The Godfather ","Francis Ford Coppola","1972",'Crime')
TAsk3=Task("Parasite","Bong Joon-ho","2019","Thriller")
print("""
        ________MOVIES LIST________\n""")
TAsk1.display_task()
TAsk2.display_task()
TAsk3.display_task()
print("Changing Movie Directors......\n\n\n")

TAsk1.mark_as_complete("Shokry Sarhan")
TAsk2.mark_as_complete("Ahmed Mazhar")
TAsk3.mark_as_complete("Isamel Yassin")

TAsk1.display_task()
TAsk2.display_task()
TAsk3.display_task()















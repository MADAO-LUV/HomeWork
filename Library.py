import datetime
import json
from typing import List, Dict

# 图书类
class Book:
    def __init__(self, title: str, author: str, isbn: str, publisher: str, entry_date: str):
        self.id = None  # 书的唯一ID
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publisher = publisher
        self.entry_date = entry_date
        self.is_borrowed = False
        self.borrower_id = None
        self.borrow_date = None

# 借阅记录类
class BorrowRecord:
    def __init__(self, book_id: int, borrower_id: str, borrow_date: str):
        self.book_id = book_id
        self.borrower_id = borrower_id
        self.borrow_date = borrow_date
        self.return_date = None

# 图书馆系统类
class LibrarySystem:
    def __init__(self):
        self.books: Dict[int, Book] = {}
        self.borrow_records: List[BorrowRecord] = []
        self.next_book_id = 1

    def add_book(self, title: str, author: str, isbn: str, publisher: str, entry_date: str):
        book = Book(title, author, isbn, publisher, entry_date)
        book.id = self.next_book_id
        self.books[self.next_book_id] = book
        self.next_book_id += 1
        print(f"该书被添加以及其ID: {book.id}")

    def borrow_book(self, book_id: int, borrower_id: str):
        if book_id not in self.books:
            print("该书ID并未存在.")
            return
        book = self.books[book_id]
        if book.is_borrowed:
            print("很抱歉，此书已经被借阅.")
            return
        book.is_borrowed = True
        book.borrower_id = borrower_id
        book.borrow_date = datetime.date.today().isoformat()
        borrow_record = BorrowRecord(book_id, borrower_id, book.borrow_date)
        self.borrow_records.append(borrow_record)
        print(f"该书被借阅: {book.title}")

    def return_book(self, book_id: int):
        if book_id not in self.books:
            print("该书ID并未存在.")
            return
        book = self.books[book_id]
        if not book.is_borrowed:
            print("该书未被借阅.")
            return
        book.is_borrowed = False
        for record in self.borrow_records:
            if record.book_id == book_id and record.return_date is None:
                record.return_date = datetime.date.today().isoformat()
                break
        print(f"图书已被归还: {book.title}")

    def search_books(self, query: str):
        results = [book for book in self.books.values() if query.lower() in book.title.lower() or query.lower() in book.author.lower() or query.lower() in book.isbn]
        if results:
            for book in results:
                status = "已被借阅" if book.is_borrowed else "可以借阅"
                print(f"本书ID: {book.id}, 书名: {book.title}, 作者: {book.author}, 借阅状态: {status}")
        else:
            print("没有找到此书.")

    def query_borrow_records(self, book_id: int):
        if book_id not in self.books:
            print("抱歉，该书ID未存在.")
            return
        records = [record for record in self.borrow_records if record.book_id == book_id]
        if records:
            for record in records:
                return_date = record.return_date if record.return_date else "抱歉，该书仍然未归还"
                print(f"借阅者 ID: {record.borrower_id}, 借阅时间: {record.borrow_date}, 归还日期: {return_date}")
        else:
            print("没有找到该书的借阅记录.")

    def save_data(self, filename: str):
        data = {
            "books": {book_id: book.__dict__ for book_id, book in self.books.items()},
            "borrow_records": [record.__dict__ for record in self.borrow_records]
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def load_data(self, filename: str):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                self.books = {int(book_id): Book(**book_data) for book_id, book_data in data["books"].items()}
                self.borrow_records = [BorrowRecord(**record_data) for record_data in data["borrow_records"]]
                self.next_book_id = max(self.books.keys(), default=0) + 1
        except FileNotFoundError:
            print("未找到图书馆该类似文件，依旧空缺")


class Visitor:
    def __init__(self, name, visitor_type):
        self.name = name
        self.visitor_type = visitor_type

    def __str__(self):
        return f"名字: {self.name}, 类型: {self.visitor_type}"


# 继承借阅者类
class Borrower(Visitor):
    def __init__(self, name, borrowed_books=None):
        super().__init__(name, "借阅者")
        self.borrowed_books = borrowed_books if borrowed_books is not None else []

    def borrow_book(self, book):
        self.borrowed_books.append(book)

    def __str__(self):
        return super().__str__() + f", 借阅书籍: {', '.join(self.borrowed_books)}"


# 管理者类
class Manager(Visitor):
    def __init__(self, name, responsibilities=None):
        super().__init__(name, "管理员")
        self.responsibilities = responsibilities if responsibilities is not None else []

    def add_responsibility(self, responsibility):
        self.responsibilities.append(responsibility)

    def __str__(self):
        return super().__str__() + f", 职责: {', '.join(self.responsibilities)}"


class PeopleSystem:
    def __init__(self):
        self.visitors = []

    def add_visitor(self, visitor):
        self.visitors.append(visitor)

    def show_visitors(self):
        for visitor in self.visitors:
            print(visitor)


def Login():
    People = PeopleSystem()
    ma = int(input("请问您是否为借阅者(1 是 / 0 否 ):"))
    if ma == 1:
        borrower = Borrower(name=input("请输入您的名字:"))
        People.add_visitor(borrower)
    else:
        manager = Manager(name=input("请输入您的名字:"))
        manager.add_responsibility(input("输入您的工作职责:"))
        People.add_visitor(manager)
    print("欢迎您的登录")


def Books():
    ma = int(input("请问您是否为借阅者(1 是 / 0 否 ):"))
    print("""
------------------图书借阅系统v1.0-----------------------
   *1. 图书信息录入(管理员进行操作)     

   *2. 图书借阅

   *3. 图书归还

   *4. 图书查询

   *5. 借阅记录查询

   *6. 登录

   *7. 退出系统
--------------------------------------------------------
        """)
    choice = int(input("请输入您的选择:"))
    lib = LibrarySystem()
    if choice == 7:
        print("感谢您的使用")
        exit()
    if ma == 0:
        if choice == 1:
            print("""
--------------正在加入图书----------------------           
            """)
            title = input("请输入书名:")
            author = input("请输入作者名字:")
            isbn = input("请输入图书的ISBN号")
            publisher = input("请输入出版社:")
            entry_date = input("进入日期(例如:2024-4-26):")
            lib.add_book(title,author,isbn,publisher,entry_date)
            print("图书加入成功")
        else:
            print("操作失误哦")
    else:
        if choice == 1:
            print("您的操作越界哦")
        if choice == 2:
            book_id = int(input("请输入图书的ID号:"))
            borrower_id = input("请输入ID:")
            lib.borrow_book(book_id,borrower_id)
        elif choice == 3:
            book_id = int(input("请输入图书的ID号"))
            lib.return_book(book_id)
            print("感谢您的及时归还，祝您生活愉快")
        elif choice == 4:
            query = input("请输入您要查找的书籍名称")
            lib.search_books(query)
        elif choice == 5:
            filename = input("请输入您要查询的书的借阅记录")
            lib.save_data(filename)

if __name__ == '__main__':
    Login()
    while(1):
        library = LibrarySystem()
        library.load_data('library_data.json')
        Books()
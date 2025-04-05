from dataclasses import dataclass


@dataclass
class Item:
    id: int
    title: str
    description: str
    price: int
    photo: str
    path: str


easy_python = Item(
    id=1,
    title="Простой Python. Билл Любанович.",
    description="Отличная книга для погружения в Python",
    price=2,
    photo="https://static.insales-cdn.com/images/products/1/2182/81324166/49602088.jpg",
    path="/app/prostoy_python.pdf",
)

networks = Item(
    id=2,
    title="Компьютерные сети. 6-е изд. Таненбаум Э., Фимстер Н., Уэзеролл Д.",
    description="Хуйня которую никто не читал , но все выебываются , что проходили в универе, и это база!",
    price=2,
    path="/app/Tanenbaum_E__Fimster_N__Uezeroll_D_-_Kompyuternye_Seti_6-E_Izd__klassika_computer_science_-_2023.pdf",
    photo="https://sun9-12.userapi.com/impg/V3HVKENj1efgBylDD0zC-QA7TpyGWVV-hw0Pmw/sPv7XaKFtKY.jpg?size=359x499&quality=96&sign=bb068fb23e24902f050b2bc024af04e2&type=album",
)

items = [easy_python, networks]

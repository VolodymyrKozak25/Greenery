LINESTRING_WIDTH = 1
POINT_AREA = 1

TAG_GROUPS = ('leisure', 'natural', 'landuse', 
              'place', 'landcover', 'barrier')

TAGS = {
    'Парк': ('leisure', 'park'),
    'Сад': ('leisure', 'garden'),
    'Місце для пікніка зі столиком': ('leisure', 'picnic_table'),
    'Природний заповідник': ('leisure', 'nature_reserve'),
    'Кущі': ('natural', 'shrubbery'),
    'Чагарники': ('natural', 'scrub'),
    'Окреме дерево': ('natural', 'tree'),
    'Ряд дерев': ('natural', 'tree_row'),
    'Група дерев': ('landcover', 'trees'),
    'Ліс (природний)': ('natural', 'wood'),
    'Лісогосподарство': ('landuse', 'forest'),
    'Трав\'яне покриття': ('landuse', 'grass'),
    'Трав\'яна територія': ('landcover', 'grass'),
    'Клумба': ('landuse', 'flowerbed'),
    'Луг, пасовище': ('landuse', 'meadow'),
    'Плодовий сад': ('landuse', 'orchard'),
    'Виноградник': ('landuse', 'vineyard'),
    'Газон': ('place', 'green'),
    'Живопліт': ('barrier', 'hedge'),
}

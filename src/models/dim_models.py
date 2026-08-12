from sqlalchemy import MetaData, Table, Column, Integer, String, Date, Numeric, Float, ForeignKey

metadata = MetaData()

# Dimensional model (star schema)
# Dimension tables
dim_customers = Table(
    'dim_customers',
    metadata,
    Column('customer_id', Integer, primary_key=True),
    Column('name', String(255)),
    Column('email', String(255)),
    Column('city', String(100)),
)

dim_products = Table(
    'dim_products',
    metadata,
    Column('product_id', Integer, primary_key=True),
    Column('name', String(255)),
    Column('category', String(100)),
    Column('price', Numeric),
)

# Fact table
fact_orders = Table(
    'fact_orders',
    metadata,
    Column('order_id', Integer, primary_key=True),
    Column('order_date', Date),
    Column('customer_id', Integer, ForeignKey('dim_customers.customer_id')),
    Column('product_id', Integer, ForeignKey('dim_products.product_id')),
    Column('quantity', Integer),
    Column('unit_price', Numeric),
    Column('total_price', Numeric),
)


def create_all_tables(engine):
    metadata.create_all(engine)


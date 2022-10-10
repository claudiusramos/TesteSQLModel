from conf.db_session import create_tables

if __name__ == '__main__':
    print("Criando tabelas...")
    try:
        create_tables()
        print("Tabelas criadas com sucesso...")
    except:
        raise

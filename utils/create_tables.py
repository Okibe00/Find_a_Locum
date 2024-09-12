'''database schema
Author:
    Okibe Ogomola Onmeje

Date:
2024-08-4
'''
TABLES = dict()
TABLES['profession'] = (
    '''
    CREATE TABLE IF NOT EXISTS profession (
    id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(25),
    created_at VARCHAR(60),
    updated_at VARCHAR(60)
    ) ENGINE=InnoDB
    '''
)

TABLES['state'] = (
    '''
    CREATE TABLE IF NOT EXISTS states (
    id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(100),
    created_at VARCHAR(60),
    updated_at VARCHAR(60)
    ) ENGINE=InnoDB
    '''
)

TABLES['city'] = (
    '''
    CREATE TABLE IF NOT EXISTS cities (
    id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(100),
    state_id VARCHAR(100),
    created_at VARCHAR(60),
    updated_at VARCHAR(60),
    FOREIGN KEY (state_id) REFERENCES states(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    INDEX (state_id)
    ) ENGINE=InnoDB
    '''
)

TABLES['user'] = (
    '''
    CREATE TABLE IF NOT EXISTS user (
    id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(255),
    gender VARCHAR(10),
    age VARCHAR(10),
    profession VARCHAR(50),
    type VARCHAR(50)
    ) ENGINE=InnoDB
    '''
)

TABLES['jobs'] = (
    '''
    CREATE TABLE IF NOT EXISTS jobs (
    id VARCHAR(100) PRIMARY KEY,
    address VARCHAR(100),
    state_id VARCHAR(100),
    city_id VARCHAR(100),
    profession_id VARCHAR(100),
    user_id VARCHAR(100),
    created_at VARCHAR(60),
    updated_at VARCHAR(60),
    description LONGTEXT,
    title TEXT,
    hourly_rate VARCHAR(50),
    status VARCHAR(10),
    hours_per_shift VARCHAR(10),
    shift VARCHAR(20),
    FOREIGN KEY (state_id) REFERENCES states(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (city_id) REFERENCES cities(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (profession_id) REFERENCES profession(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (user_id) REFERENCES user(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    INDEX idx_jobs_state_city_user (state_id, city_id, profession_id, user_id),
    INDEX idx_title (title)
    ) ENGINE=InnoDB
    '''
)


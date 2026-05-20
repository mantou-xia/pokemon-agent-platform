-- Pokemon Core Tables for Dify Agent Platform
-- Run against the existing Dify PostgreSQL database

-- Types (属性)
CREATE TABLE IF NOT EXISTS pokemon_types (
    id          SERIAL PRIMARY KEY,
    name_zh     VARCHAR(20) NOT NULL,       -- 中文名，如 "火"
    name_en     VARCHAR(20) NOT NULL,       -- 英文名，如 "fire"
    color       VARCHAR(7)  NOT NULL DEFAULT '#999999'
);

-- Type effectiveness (属性克制)
CREATE TABLE IF NOT EXISTS type_effectiveness (
    attacking_type_id  INT NOT NULL REFERENCES pokemon_types(id),
    defending_type_id  INT NOT NULL REFERENCES pokemon_types(id),
    multiplier         DECIMAL(3,1) NOT NULL DEFAULT 1.0,  -- 2.0, 0.5, 0.0
    PRIMARY KEY (attacking_type_id, defending_type_id)
);

-- Abilities (特性)
CREATE TABLE IF NOT EXISTS abilities (
    id          SERIAL PRIMARY KEY,
    name_zh     VARCHAR(50) NOT NULL,
    name_en     VARCHAR(50) NOT NULL,
    description TEXT
);

-- Moves (技能)
CREATE TABLE IF NOT EXISTS moves (
    id          SERIAL PRIMARY KEY,
    name_zh     VARCHAR(50) NOT NULL,
    name_en     VARCHAR(50) NOT NULL,
    type_id     INT REFERENCES pokemon_types(id),
    power       INT,                    -- 威力，无威力技能为 NULL
    accuracy    INT,                    -- 命中率，必中为 NULL
    pp          INT,                    -- PP 值
    damage_class VARCHAR(20),           -- physical / special / status
    description TEXT
);

-- Pokemon 基础信息
CREATE TABLE IF NOT EXISTS pokemon (
    id              SERIAL PRIMARY KEY,
    national_id     INT UNIQUE NOT NULL,   -- 全国图鉴编号
    name_zh         VARCHAR(50) NOT NULL,
    name_en         VARCHAR(50) NOT NULL,
    type1_id        INT NOT NULL REFERENCES pokemon_types(id),
    type2_id        INT REFERENCES pokemon_types(id),
    hp              INT NOT NULL,
    attack          INT NOT NULL,
    defense         INT NOT NULL,
    sp_attack       INT NOT NULL,
    sp_defense      INT NOT NULL,
    speed           INT NOT NULL,
    ability1_id     INT REFERENCES abilities(id),
    ability2_id     INT REFERENCES abilities(id),
    hidden_ability_id INT REFERENCES abilities(id),
    evolves_from    INT REFERENCES pokemon(national_id),
    description     TEXT
);

-- Evolution chains (进化链)
CREATE TABLE IF NOT EXISTS evolution_chains (
    id              SERIAL PRIMARY KEY,
    pokemon_id      INT NOT NULL REFERENCES pokemon(national_id),
    evolves_to      INT REFERENCES pokemon(national_id),
    trigger_method  VARCHAR(30),         -- level-up / trade / stone / etc
    trigger_detail  VARCHAR(100),        -- 触发条件详情，如 "level 36"
    chain_order     INT NOT NULL DEFAULT 0  -- 在进化链中的顺序
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_pokemon_name_zh ON pokemon(name_zh);
CREATE INDEX IF NOT EXISTS idx_pokemon_name_en ON pokemon(name_en);
CREATE INDEX IF NOT EXISTS idx_moves_name_zh ON moves(name_zh);
CREATE INDEX IF NOT EXISTS idx_moves_name_en ON moves(name_en);

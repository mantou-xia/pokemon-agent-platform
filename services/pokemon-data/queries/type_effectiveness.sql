-- 查询属性克制关系
-- SELECT * FROM type_effectiveness_view WHERE attacking_type = '火';

CREATE OR REPLACE VIEW type_effectiveness_view AS
SELECT 
    a.name_zh AS attacking_type,
    d.name_zh AS defending_type,
    te.multiplier,
    CASE 
        WHEN te.multiplier = 0.0 THEN '无效果（免疫）'
        WHEN te.multiplier = 0.25 THEN '效果极差'
        WHEN te.multiplier = 0.5 THEN '效果不好'
        WHEN te.multiplier = 1.0 THEN '效果普通'
        WHEN te.multiplier = 2.0 THEN '效果拔群'
        WHEN te.multiplier = 4.0 THEN '效果极佳'
    END AS description
FROM type_effectiveness te
JOIN pokemon_types a ON te.attacking_type_id = a.id
JOIN pokemon_types d ON te.defending_type_id = d.id;

-- 查询宝可梦属性克制：SELECT * FROM pokemon_weakness_view WHERE pokemon_name = '喷火龙';
CREATE OR REPLACE VIEW pokemon_weakness_view AS
SELECT 
    p.name_zh AS pokemon_name,
    t.name_zh AS defending_type,
    te_att.name_zh AS attacking_type,
    te.multiplier
FROM pokemon p
JOIN pokemon_types t ON t.id IN (p.type1_id)
LEFT JOIN type_effectiveness te ON te.defending_type_id = t.id
JOIN pokemon_types te_att ON te.attacking_type_id = te_att.id
WHERE te.multiplier IS NOT NULL
UNION ALL
SELECT 
    p.name_zh AS pokemon_name,
    t.name_zh AS defending_type,
    te_att.name_zh AS attacking_type,
    te.multiplier
FROM pokemon p
JOIN pokemon_types t ON t.id = p.type2_id
LEFT JOIN type_effectiveness te ON te.defending_type_id = t.id
JOIN pokemon_types te_att ON te.attacking_type_id = te_att.id
WHERE te.multiplier IS NOT NULL AND p.type2_id IS NOT NULL;

-- 查询进化链：SELECT * FROM evolution_chain_view WHERE base_pokemon = '伊布';
CREATE OR REPLACE VIEW evolution_chain_view AS
WITH RECURSIVE chain AS (
    SELECT 
        p.national_id AS base_id,
        p.name_zh AS base_pokemon,
        ec.evolves_to,
        ec.trigger_method,
        ec.trigger_detail,
        ec.chain_order
    FROM pokemon p
    LEFT JOIN evolution_chains ec ON p.national_id = ec.pokemon_id
    WHERE p.evolves_from IS NULL
    
    UNION ALL
    
    SELECT 
        c.base_id,
        c.base_pokemon,
        ec.evolves_to,
        ec.trigger_method,
        ec.trigger_detail,
        ec.chain_order
    FROM chain c
    JOIN evolution_chains ec ON ec.pokemon_id = c.evolves_to
)
SELECT * FROM chain ORDER BY base_id, chain_order;

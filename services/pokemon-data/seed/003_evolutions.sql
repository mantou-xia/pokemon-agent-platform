-- Seed Data: Evolution Chains (Gen1)

INSERT INTO evolution_chains (pokemon_id, evolves_to, trigger_method, trigger_detail, chain_order) VALUES
    (1, 2, 'level-up', 'level 16', 1),
    (2, 3, 'level-up', 'level 32', 2),
    (4, 5, 'level-up', 'level 16', 1),
    (5, 6, 'level-up', 'level 36', 2),
    (7, 8, 'level-up', 'level 16', 1),
    (8, 9, 'level-up', 'level 36', 2),
    (52, 53, 'level-up', 'level 28', 1),
    (54, 55, 'level-up', 'level 33', 1),
    (58, 59, 'level-up', 'use Fire Stone', 1),
    (63, 64, 'level-up', 'level 16', 1),
    (64, 65, 'trade', NULL, 2),
    (92, 93, 'level-up', 'level 25', 1),
    (93, 94, 'trade', NULL, 2),
    (129, 130, 'level-up', 'level 20', 1),
    (133, 134, 'level-up', 'use Water Stone', 1),
    (133, 135, 'level-up', 'use Thunder Stone', 1),
    (133, 136, 'level-up', 'use Fire Stone', 1),
    (147, 148, 'level-up', 'level 30', 1),
    (148, 149, 'level-up', 'level 55', 2)
ON CONFLICT DO NOTHING;

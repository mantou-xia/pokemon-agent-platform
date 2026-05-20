-- Reset admin account
INSERT INTO accounts (id, name, email, password, password_salt, status, initialized_at, interface_language)
VALUES ('bcdb21dd-30e8-403f-9000-5b874a217af2', E'\u9992\u5934\u867e', '3775060926@qq.com', 'NWFhODE1NjZkYzkxN2M0NzRkOGZmNjRkNjJjYWZlYzcyMDM5NTJjNDQxY2U1YjY0OTMyNDgyZThjMWRiOGJlYw==', 'vtjIB1UnxSoLhYcB2DhY1A==', 'active', NOW(), 'zh-Hans')
ON CONFLICT (id) DO UPDATE SET password = EXCLUDED.password, password_salt = EXCLUDED.password_salt;

INSERT INTO tenant_account_joins (tenant_id, account_id, role)
VALUES ('1e4938b2-235f-48eb-b2c8-252cbf6d4c76', 'bcdb21dd-30e8-403f-9000-5b874a217af2', 'owner')
ON CONFLICT DO NOTHING;

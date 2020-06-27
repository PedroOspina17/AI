CREATE TABLE customer (id serial not null, created_at date, is_premier boolean, is_spam boolean, CONSTRAINT customer_pkey PRIMARY KEY (id));
CREATE TABLE score (id serial not null, customer_id integer references customer(id), created_at date, score integer, CONSTRAINT scores_pkey PRIMARY KEY (id));
COPY customer FROM 'customer.csv' WITH (format csv, header true, delimiter ',');
COPY score FROM 'score.csv' WITH (format csv, header true, delimiter ',');
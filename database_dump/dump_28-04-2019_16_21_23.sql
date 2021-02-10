--
-- PostgreSQL database cluster dump
--

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Drop databases (except postgres and template1)
--

DROP DATABASE guided_tours;




--
-- Drop roles
--

DROP ROLE postgres;


--
-- Roles
--

CREATE ROLE postgres;
ALTER ROLE postgres WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION BYPASSRLS PASSWORD 'md55af40ebf946f20cd197a510a6b97ccc9';






--
-- PostgreSQL database dump
--

-- Dumped from database version 11.2 (Debian 11.2-1.pgdg90+1)
-- Dumped by pg_dump version 11.2 (Debian 11.2-1.pgdg90+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

UPDATE pg_catalog.pg_database SET datistemplate = false WHERE datname = 'template1';
DROP DATABASE template1;
--
-- Name: template1; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE template1 WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.utf8' LC_CTYPE = 'en_US.utf8';


ALTER DATABASE template1 OWNER TO postgres;

\connect template1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: DATABASE template1; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON DATABASE template1 IS 'default template for new databases';


--
-- Name: template1; Type: DATABASE PROPERTIES; Schema: -; Owner: postgres
--

ALTER DATABASE template1 IS_TEMPLATE = true;


\connect template1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: DATABASE template1; Type: ACL; Schema: -; Owner: postgres
--

REVOKE CONNECT,TEMPORARY ON DATABASE template1 FROM PUBLIC;
GRANT CONNECT ON DATABASE template1 TO PUBLIC;


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 11.2 (Debian 11.2-1.pgdg90+1)
-- Dumped by pg_dump version 11.2 (Debian 11.2-1.pgdg90+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: guided_tours; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE guided_tours WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.utf8' LC_CTYPE = 'en_US.utf8';


ALTER DATABASE guided_tours OWNER TO postgres;

\connect guided_tours

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: accounts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accounts (
    id integer NOT NULL,
    created_at timestamp without time zone NOT NULL,
    suspended boolean,
    closed boolean,
    closed_at timestamp without time zone,
    user_id integer NOT NULL
);


ALTER TABLE public.accounts OWNER TO postgres;

--
-- Name: accounts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.accounts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.accounts_id_seq OWNER TO postgres;

--
-- Name: accounts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.accounts_id_seq OWNED BY public.accounts.id;


--
-- Name: sessions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sessions (
    id integer NOT NULL,
    last_login timestamp without time zone,
    last_logout timestamp without time zone,
    user_id integer NOT NULL
);


ALTER TABLE public.sessions OWNER TO postgres;

--
-- Name: sessions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sessions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sessions_id_seq OWNER TO postgres;

--
-- Name: sessions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sessions_id_seq OWNED BY public.sessions.id;


--
-- Name: tour_content; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tour_content (
    id integer NOT NULL,
    key character varying(50) NOT NULL,
    name character varying(120) NOT NULL,
    content_type character varying(25) NOT NULL,
    extension character varying(10) NOT NULL,
    tour_id integer NOT NULL
);


ALTER TABLE public.tour_content OWNER TO postgres;

--
-- Name: tour_content_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tour_content_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tour_content_id_seq OWNER TO postgres;

--
-- Name: tour_content_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tour_content_id_seq OWNED BY public.tour_content.id;


--
-- Name: tour_details; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tour_details (
    id integer NOT NULL,
    title character varying(50) NOT NULL,
    description character varying(255) NOT NULL,
    latitude numeric NOT NULL,
    longitude numeric NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.tour_details OWNER TO postgres;

--
-- Name: tour_details_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tour_details_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tour_details_id_seq OWNER TO postgres;

--
-- Name: tour_details_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tour_details_id_seq OWNED BY public.tour_details.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(16) NOT NULL,
    email character varying(120) NOT NULL,
    password character varying(255) NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: accounts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts ALTER COLUMN id SET DEFAULT nextval('public.accounts_id_seq'::regclass);


--
-- Name: sessions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sessions ALTER COLUMN id SET DEFAULT nextval('public.sessions_id_seq'::regclass);


--
-- Name: tour_content id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tour_content ALTER COLUMN id SET DEFAULT nextval('public.tour_content_id_seq'::regclass);


--
-- Name: tour_details id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tour_details ALTER COLUMN id SET DEFAULT nextval('public.tour_details_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: accounts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accounts (id, created_at, suspended, closed, closed_at, user_id) FROM stdin;
1	2019-04-27 11:53:54.663266	f	f	\N	1
2	2019-04-28 10:05:26.18888	f	f	\N	2
3	2019-04-28 14:55:54.696642	f	f	\N	3
4	2019-04-28 14:55:54.696642	f	f	\N	4
5	2019-04-28 15:01:00.00495	f	f	\N	5
\.


--
-- Data for Name: sessions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sessions (id, last_login, last_logout, user_id) FROM stdin;
1	2019-04-27 11:53:54.646076	\N	1
2	2019-04-27 11:53:54.646076	\N	1
3	2019-04-27 11:53:54.646076	\N	1
4	2019-04-27 11:53:54.646076	\N	1
5	2019-04-27 11:53:54.646076	\N	1
6	2019-04-27 11:53:54.646076	\N	1
7	2019-04-27 11:53:54.646076	\N	1
15	2019-04-28 10:05:26.170659	\N	1
16	2019-04-28 10:05:26.170659	\N	1
9	2019-04-28 10:05:26.170659	2019-04-28 11:15:03.033807	1
17	2019-04-28 10:05:26.170659	\N	1
18	2019-04-28 10:05:26.170659	\N	1
10	2019-04-28 10:05:26.170659	2019-04-28 11:27:10.846969	1
19	2019-04-28 10:05:26.170659	\N	1
11	2019-04-28 10:05:26.170659	2019-04-28 11:28:18.743746	1
20	2019-04-28 10:05:26.170659	\N	1
21	2019-04-28 10:05:26.170659	\N	1
22	2019-04-28 10:05:26.170659	\N	1
23	2019-04-28 10:05:26.170659	\N	1
24	2019-04-28 10:05:26.170659	\N	1
25	2019-04-28 10:05:26.170659	\N	1
26	2019-04-28 10:05:26.170659	\N	1
27	2019-04-28 10:05:26.170659	\N	1
28	2019-04-28 10:05:26.170659	\N	1
29	2019-04-28 10:05:26.170659	\N	1
30	2019-04-28 10:05:26.170659	\N	1
31	2019-04-28 10:05:26.170659	\N	1
12	2019-04-28 10:05:26.170659	2019-04-28 12:10:47.460525	1
32	2019-04-28 10:05:26.170659	\N	1
33	2019-04-28 10:05:26.170659	\N	1
34	2019-04-28 10:05:26.170659	\N	1
35	2019-04-28 10:05:26.170659	\N	1
36	2019-04-28 10:05:26.170659	\N	1
37	2019-04-28 10:05:26.170659	\N	1
38	2019-04-28 10:05:26.170659	\N	1
39	2019-04-28 10:05:26.170659	\N	1
40	2019-04-28 10:05:26.170659	\N	1
41	2019-04-28 10:05:26.170659	\N	1
13	2019-04-28 10:05:26.170659	2019-04-28 12:28:41.901664	1
42	2019-04-28 10:05:26.170659	\N	1
14	2019-04-28 10:05:26.170659	2019-04-28 12:34:58.345257	1
43	2019-04-28 10:05:26.170659	\N	1
8	2019-04-28 10:05:26.170659	2019-04-28 12:37:29.339182	1
44	2019-04-28 10:05:26.170659	\N	1
45	2019-04-28 10:05:26.170659	\N	1
46	2019-04-28 10:05:26.170659	\N	1
47	2019-04-28 10:05:26.170659	\N	1
48	2019-04-28 10:05:26.170659	\N	1
49	2019-04-28 10:05:26.170659	\N	1
50	2019-04-28 10:05:26.170659	\N	1
51	2019-04-28 10:05:26.170659	\N	1
52	2019-04-28 10:05:26.170659	\N	1
53	2019-04-28 10:05:26.170659	\N	1
54	2019-04-28 10:05:26.170659	\N	1
55	2019-04-28 10:05:26.170659	\N	1
56	2019-04-28 10:05:26.170659	\N	1
57	2019-04-28 10:05:26.170659	\N	1
58	2019-04-28 10:05:26.170659	\N	1
59	2019-04-28 10:05:26.170659	\N	1
60	2019-04-28 10:05:26.170659	\N	1
61	2019-04-28 10:05:26.170659	\N	1
62	2019-04-28 10:05:26.170659	\N	1
63	2019-04-28 10:05:26.170659	\N	1
64	2019-04-28 10:05:26.170659	\N	1
65	2019-04-28 10:05:26.170659	\N	1
66	2019-04-28 10:05:26.170659	\N	1
67	2019-04-28 10:05:26.170659	\N	1
68	2019-04-28 10:05:26.170659	\N	1
69	2019-04-28 10:05:26.170659	\N	1
70	2019-04-28 10:05:26.170659	\N	2
71	2019-04-28 14:55:54.681935	2019-04-28 14:59:28.41131	3
72	2019-04-28 14:55:54.681935	2019-04-28 15:01:03.575299	4
73	2019-04-28 15:00:59.985818	\N	5
74	2019-04-28 15:18:34.709681	\N	1
76	2019-04-28 15:42:17.9024	\N	1
75	2019-04-28 15:42:17.9024	2019-04-28 15:48:47.829152	1
\.


--
-- Data for Name: tour_content; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tour_content (id, key, name, content_type, extension, tour_id) FROM stdin;
7	audioContent	Aretha Franklin - Respect [1967] (Original Version).mp3	audio/mpeg	.mp3	9
8	image0	Selection_005.png	image/png	.png	9
9	audioContent	Aretha Franklin - Respect [1967] (Original Version).mp3	audio/mpeg	.mp3	10
10	image0	Selection_005.png	image/png	.png	10
11	audioContent	Aretha Franklin - Respect [1967] (Original Version).mp3	audio/mpeg	.mp3	11
12	image0	Selection_005.png	image/png	.png	11
13	audioContent	Aretha Franklin - Respect [1967] (Original Version).mp3	audio/mpeg	.mp3	12
14	image0	Selection_005.png	image/png	.png	12
15	audioContent	Aretha Franklin - Respect [1967] (Original Version).mp3	audio/mpeg	.mp3	13
16	image0	Selection_005.png	image/png	.png	13
17	audioContent	Aretha Franklin - Respect [1967] (Original Version).mp3	audio/mpeg	.mp3	14
18	image0	Selection_005.png	image/png	.png	14
19	audioContent	Aretha Franklin - Respect [1967] (Original Version).mp3	audio/mpeg	.mp3	15
20	image0	Selection_005.png	image/png	.png	15
21	audioContent	Aretha Franklin - Respect [1967] (Original Version).mp3	audio/mpeg	.mp3	16
22	image0	Selection_005.png	image/png	.png	16
23	audioContent	Aretha Franklin - Respect [1967] (Original Version).mp3	audio/mpeg	.mp3	17
24	image0	Selection_005.png	image/png	.png	17
25	audioContent	Aretha Franklin - Respect [1967] (Original Version).mp3	audio/mpeg	.mp3	18
26	image0	Selection_005.png	image/png	.png	18
\.


--
-- Data for Name: tour_details; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tour_details (id, title, description, latitude, longitude, user_id) FROM stdin;
10	test jjjj	test jjjj	53.2923890568628166874987073242664337158203125	-6.13796138413090375252068042755126953125	1
11	cccccccccccccc	ccccccccccccccc	53.29141427508555040049031958915293216705322265625	-6.13933467514652875252068042755126953125	1
12	aaaaaaaaaaa	aaaaaaaaaa	53.292799484641051321887061931192874908447265625	-6.13856219895023969002068042755126953125	1
13	hjjkkkkkkkkkkkk	scvvvvvvvvvv	53.2913629701653377424008795060217380523681640625	-6.13581561691898969002068042755126953125	1
14	jsj3eihfewa	jsj3eihfewa	53.29254296774174548545488505624234676361083984375	-6.13787555344242719002068042755126953125	1
15	testttttt	testttttt	53.29192732089884287915992899797856807708740234375	-6.14087962753910687752068042755126953125	1
16	test trr	test trr	53.29254296774174548545488505624234676361083984375	-6.14010715134281781502068042755126953125	1
17	andrea tour	andrea tour	53.30228952708977629981745849363505840301513671875	-6.12663173325199750252068042755126953125	2
18	klwjdocsa	klwjdocsa	53.29290209096948416345185250975191593170166015625	-6.13967799790043500252068042755126953125	1
9	666666test tour uploading 26666666666	test tour uploading 2	53.29202992932214755228415015153586864471435546875	-6.13821887619633344002068042755126953125	1
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, email, password) FROM stdin;
1	lorcan	lorcan@gmail.com	$pbkdf2-sha256$29000$lNJ6z5nTOiektDaGMIawdg$JKwwubY5MxjV8JDo5r3WxAtkOMbHLGz29NXkQPHCMUo
2	andrea	andrea@gmail.com	$pbkdf2-sha256$29000$4ByjdG4NgVDKWQsBIATAGA$zGSND5svUXtPl3U4wZh1dEA3q7pKGn0YCt2bS5H.Uac
3	teste	test@test.com	$pbkdf2-sha256$29000$mLP2/p.TkhLinJMSorTWug$wV5gRKverobRRwQhJ2JYFTBKZXvabH9315rMiWD.URk
4	henn	henn@henn.com	$pbkdf2-sha256$29000$ZYyRsva.NyZk7P0/B.Ac4w$tYH/xt3LeObXANwEm1KdUdZFMzpgnfcuR5V3eidYXEk
5	john	john@john.com	$pbkdf2-sha256$29000$L8XYe89ZqzWmtBZizHmv9Q$H5zdTWaoa4dPGDZrZD2V/ZWFyJU8Ctc7kr/POernAy8
\.


--
-- Name: accounts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accounts_id_seq', 5, true);


--
-- Name: sessions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sessions_id_seq', 76, true);


--
-- Name: tour_content_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tour_content_id_seq', 26, true);


--
-- Name: tour_details_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tour_details_id_seq', 18, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 5, true);


--
-- Name: accounts accounts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_pkey PRIMARY KEY (id);


--
-- Name: sessions sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_pkey PRIMARY KEY (id);


--
-- Name: tour_content tour_content_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tour_content
    ADD CONSTRAINT tour_content_pkey PRIMARY KEY (id);


--
-- Name: tour_details tour_details_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tour_details
    ADD CONSTRAINT tour_details_pkey PRIMARY KEY (id);


--
-- Name: tour_details tour_details_title_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tour_details
    ADD CONSTRAINT tour_details_title_key UNIQUE (title);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: accounts accounts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: sessions sessions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: tour_content tour_content_tour_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tour_content
    ADD CONSTRAINT tour_content_tour_id_fkey FOREIGN KEY (tour_id) REFERENCES public.tour_details(id) ON DELETE CASCADE;


--
-- Name: tour_details tour_details_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tour_details
    ADD CONSTRAINT tour_details_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 11.2 (Debian 11.2-1.pgdg90+1)
-- Dumped by pg_dump version 11.2 (Debian 11.2-1.pgdg90+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE postgres;
--
-- Name: postgres; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE postgres WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.utf8' LC_CTYPE = 'en_US.utf8';


ALTER DATABASE postgres OWNER TO postgres;

\connect postgres

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: DATABASE postgres; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON DATABASE postgres IS 'default administrative connection database';


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database cluster dump complete
--


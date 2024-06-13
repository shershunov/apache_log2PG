PGDMP  1                    |         
   internship    15.6 (Debian 15.6-0+deb12u1)    16.3                0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false                       1262    16387 
   internship    DATABASE     v   CREATE DATABASE internship WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.UTF-8';
    DROP DATABASE internship;
                postgres    false            �            1255    16417    apache_log_delete(bigint) 	   PROCEDURE     �   CREATE PROCEDURE public.apache_log_delete(IN p_id_apache_logs bigint)
    LANGUAGE plpgsql
    AS $$
BEGIN
    DELETE FROM apache_logs
    WHERE id_apache_logs = p_id_apache_logs;
END;
$$;
 E   DROP PROCEDURE public.apache_log_delete(IN p_id_apache_logs bigint);
       public          postgres    false            �            1255    16415 V   apache_log_insert(character varying, timestamp with time zone, text, integer, integer) 	   PROCEDURE     �  CREATE PROCEDURE public.apache_log_insert(IN p_ip_address character varying, IN p_timestamp timestamp with time zone, IN p_request text, IN p_status_code integer, IN p_response_size integer)
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO apache_logs (ip_address, timestamp, request, status_code, response_size)
    VALUES (p_ip_address, p_timestamp, p_request, p_status_code, p_response_size);
END;
$$;
 �   DROP PROCEDURE public.apache_log_insert(IN p_ip_address character varying, IN p_timestamp timestamp with time zone, IN p_request text, IN p_status_code integer, IN p_response_size integer);
       public          postgres    false                       0    0 �   PROCEDURE apache_log_insert(IN p_ip_address character varying, IN p_timestamp timestamp with time zone, IN p_request text, IN p_status_code integer, IN p_response_size integer)    ACL     �   GRANT ALL ON PROCEDURE public.apache_log_insert(IN p_ip_address character varying, IN p_timestamp timestamp with time zone, IN p_request text, IN p_status_code integer, IN p_response_size integer) TO watchdog_agent;
          public          postgres    false    217            �            1255    16440 \   apache_log_insert(character varying, text, timestamp with time zone, text, integer, integer) 	   PROCEDURE     �  CREATE PROCEDURE public.apache_log_insert(IN p_ip_address character varying, IN p_log_name text, IN p_timestamp timestamp with time zone, IN p_request text, IN p_status_code integer, IN p_response_size integer)
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO apache_logs (ip_address, log_name, timestamp, request, status_code, response_size)
    VALUES (p_ip_address, p_log_name, p_timestamp, p_request, p_status_code, p_response_size);
END;
$$;
 �   DROP PROCEDURE public.apache_log_insert(IN p_ip_address character varying, IN p_log_name text, IN p_timestamp timestamp with time zone, IN p_request text, IN p_status_code integer, IN p_response_size integer);
       public          postgres    false            �            1255    16416 ^   apache_log_update(bigint, character varying, timestamp with time zone, text, integer, integer) 	   PROCEDURE     �  CREATE PROCEDURE public.apache_log_update(IN p_id_apache_logs bigint, IN p_ip_address character varying, IN p_timestamp timestamp with time zone, IN p_request text, IN p_status_code integer, IN p_response_size integer)
    LANGUAGE plpgsql
    AS $$
BEGIN
    UPDATE apache_logs
    SET ip_address = p_ip_address,
        timestamp = p_timestamp,
        request = p_request,
        status_code = p_status_code,
        response_size = p_response_size
    WHERE id_apache_logs = p_id_apache_logs;
END;
$$;
 �   DROP PROCEDURE public.apache_log_update(IN p_id_apache_logs bigint, IN p_ip_address character varying, IN p_timestamp timestamp with time zone, IN p_request text, IN p_status_code integer, IN p_response_size integer);
       public          postgres    false            �            1255    16441 d   apache_log_update(bigint, character varying, text, timestamp with time zone, text, integer, integer) 	   PROCEDURE     .  CREATE PROCEDURE public.apache_log_update(IN p_id_apache_logs bigint, IN p_ip_address character varying, IN p_log_name text, IN p_timestamp timestamp with time zone, IN p_request text, IN p_status_code integer, IN p_response_size integer)
    LANGUAGE plpgsql
    AS $$
BEGIN
    UPDATE apache_logs
    SET ip_address = p_ip_address,
        log_name = p_log_name,
        timestamp = p_timestamp,
        request = p_request,
        status_code = p_status_code,
        response_size = p_response_size
    WHERE id_apache_logs = p_id_apache_logs;
END;
$$;
 �   DROP PROCEDURE public.apache_log_update(IN p_id_apache_logs bigint, IN p_ip_address character varying, IN p_log_name text, IN p_timestamp timestamp with time zone, IN p_request text, IN p_status_code integer, IN p_response_size integer);
       public          postgres    false            �            1259    16431    apache_logs    TABLE     '  CREATE TABLE public.apache_logs (
    id_apache_logs bigint NOT NULL,
    ip_address character varying(45) NOT NULL,
    log_name text NOT NULL,
    "timestamp" timestamp with time zone NOT NULL,
    request text NOT NULL,
    status_code integer NOT NULL,
    response_size integer NOT NULL
);
    DROP TABLE public.apache_logs;
       public         heap    postgres    false                       0    0    TABLE apache_logs    ACL     �   GRANT SELECT,INSERT,UPDATE ON TABLE public.apache_logs TO watchdog_agent;
GRANT SELECT ON TABLE public.apache_logs TO api_agent;
          public          postgres    false    215            �            1259    16430    apache_logs_id_apache_logs_seq    SEQUENCE     �   CREATE SEQUENCE public.apache_logs_id_apache_logs_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 5   DROP SEQUENCE public.apache_logs_id_apache_logs_seq;
       public          postgres    false    215                        0    0    apache_logs_id_apache_logs_seq    SEQUENCE OWNED BY     a   ALTER SEQUENCE public.apache_logs_id_apache_logs_seq OWNED BY public.apache_logs.id_apache_logs;
          public          postgres    false    214            !           0    0 '   SEQUENCE apache_logs_id_apache_logs_seq    ACL     X   GRANT SELECT,USAGE ON SEQUENCE public.apache_logs_id_apache_logs_seq TO watchdog_agent;
          public          postgres    false    214            �           2604    16434    apache_logs id_apache_logs    DEFAULT     �   ALTER TABLE ONLY public.apache_logs ALTER COLUMN id_apache_logs SET DEFAULT nextval('public.apache_logs_id_apache_logs_seq'::regclass);
 I   ALTER TABLE public.apache_logs ALTER COLUMN id_apache_logs DROP DEFAULT;
       public          postgres    false    215    214    215                      0    16431    apache_logs 
   TABLE DATA           }   COPY public.apache_logs (id_apache_logs, ip_address, log_name, "timestamp", request, status_code, response_size) FROM stdin;
    public          postgres    false    215   C!       "           0    0    apache_logs_id_apache_logs_seq    SEQUENCE SET     M   SELECT pg_catalog.setval('public.apache_logs_id_apache_logs_seq', 1, false);
          public          postgres    false    214            �           2606    16438    apache_logs pk_apache_logs 
   CONSTRAINT     d   ALTER TABLE ONLY public.apache_logs
    ADD CONSTRAINT pk_apache_logs PRIMARY KEY (id_apache_logs);
 D   ALTER TABLE ONLY public.apache_logs DROP CONSTRAINT pk_apache_logs;
       public            postgres    false    215            �           1259    16439    index_id_apache_logs    INDEX     V   CREATE INDEX index_id_apache_logs ON public.apache_logs USING btree (id_apache_logs);
 (   DROP INDEX public.index_id_apache_logs;
       public            postgres    false    215                  x������ � �     
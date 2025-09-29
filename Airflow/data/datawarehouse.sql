DROP TYPE IF EXISTS public.status_proposta CASCADE;
CREATE TYPE public.status_proposta AS ENUM (
    'Enviada',
    'Validação documentos',
    'Aprovada',
    'Reprovada',
    'Em análise'
);


--
-- Name: tipo_agencia; Type: TYPE; Schema: public; Owner: -
--

DROP TYPE IF EXISTS public.tipo_agencia CASCADE;
CREATE TYPE public.tipo_agencia AS ENUM (
    'Digital',
    'Física'
);


--
-- Name: tipo_cliente; Type: TYPE; Schema: public; Owner: -
--

DROP TYPE IF EXISTS public.tipo_cliente CASCADE;
CREATE TYPE public.tipo_cliente AS ENUM (
    'PF',
    'PJ'
);


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: agencias; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE IF NOT EXISTS public.agencias (
    cod_agencia integer NOT NULL,
    nome character varying(255) NOT NULL,
    endereco text,
    cidade character varying(255),
    uf character(2),
    data_abertura date,
    tipo_agencia public.tipo_agencia
);


--
-- Name: clientes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE IF NOT EXISTS public.clientes (
    cod_cliente integer NOT NULL,
    primeiro_nome character varying(255) NOT NULL,
    ultimo_nome character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    tipo_cliente public.tipo_cliente,
    data_inclusao timestamp with time zone,
    cpfcnpj character varying(18) NOT NULL,
    data_nascimento date,
    endereco text,
    cep character varying(9)
);


--
-- Name: colaborador_agencia; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE IF NOT EXISTS public.colaborador_agencia (
    cod_colaborador integer NOT NULL,
    cod_agencia integer NOT NULL
);


--
-- Name: colaboradores; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE IF NOT EXISTS public.colaboradores (
    cod_colaborador integer NOT NULL,
    primeiro_nome character varying(255) NOT NULL,
    ultimo_nome character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    cpf character varying(14) NOT NULL,
    data_nascimento date,
    endereco text,
    cep character varying(9)
);


--
-- Name: contas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE IF NOT EXISTS public.contas (
    num_conta bigint NOT NULL,
    cod_cliente integer,
    cod_agencia integer,
    cod_colaborador integer,
    tipo_conta public.tipo_cliente,
    data_abertura timestamp with time zone,
    saldo_total numeric(15,2),
    saldo_disponivel numeric(15,2),
    data_ultimo_lancamento timestamp with time zone
);


--
-- Name: propostas_credito; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE IF NOT EXISTS public.propostas_credito (
    cod_proposta integer NOT NULL,
    cod_cliente integer,
    cod_colaborador integer,
    data_entrada_proposta timestamp with time zone,
    taxa_juros_mensal numeric(5,4),
    valor_proposta numeric(15,2),
    valor_financiamento numeric(15,2),
    valor_entrada numeric(15,2),
    valor_prestacao numeric(15,2),
    quantidade_parcelas integer,
    carencia integer,
    status_proposta public.status_proposta
);

--
-- Name: transacoes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE IF NOT EXISTS public.transacoes(
    cod_transacao bigint NOT NULL,
    num_conta bigint,
    data_transacao timestamp with time zone,
    nome_transacao character varying(100),
    valor_transacao numeric(15,2)
);



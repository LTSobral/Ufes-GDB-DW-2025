CREATE TABLE dw.d_tipo_consumidor (
    sk_tipo_consumidor INTEGER PRIMARY KEY,
    cd_tipo_consumidor VARCHAR(20),
    no_tipo_consumidor VARCHAR(20),
    no_classe_consumo VARCHAR(20),
    dt_atualizacao TIMESTAMP
);

COMMENT ON COLUMN dw.d_tipo_consumidor.sk_tipo_consumidor IS 'Chave primária da dimensão classe de consumo.';
COMMENT ON COLUMN dw.d_tipo_consumidor.no_classe IS 'Descrição da classificação de consumo das unidades consumidoras. Mapeado de: DscClasse Consumo.';
-- cd_tipo_consumidor VARCHAR(20),
-- no_tipo_consumidor VARCHAR(20),
COMMENT ON COLUMN dw.d_tipo_consumidor.dt_atualizacao IS 'Data da última atualização do registro.';

----------------------------------------------------------------------------------------------------

CREATE TABLE dw.d_grupo_tarifario (
    sk_grupo_tarifario INTEGER PRIMARY KEY,
    cd_grupo_tarifario VARCHAR(20),
    ds_grupo_tarifario VARCHAR(50),
    dt_atualizacao TIMESTAMP
);

COMMENT ON COLUMN dw.d_grupo_tarifario.sk_grupo_tarifario IS 'Chave primária da dimensão classe de grupo tarifario.';
COMMENT ON COLUMN dw.d_grupo_tarifario.cd_grupo_tarifario IS 'Código que representa os subgrupos tarifários. Mapeado de: CodSubGrupo Tarifario.';
COMMENT ON COLUMN dw.d_grupo_tarifario.ds_grupo_tarifario IS 'Descrição dos subgrupos tarifários (A1, A2, B1, etc.). Mapeado de: DscSubGrupo Tarifario.';
COMMENT ON COLUMN dw.d_grupo_tarifario.dt_atualizacao IS 'Data da última atualização do registro.';

----------------------------------------------------------------------------------------------------

CREATE TABLE dw.d_empresa_distribuidora (
    sk_empresa_distribuidora INTEGER PRIMARY KEY,
    cd_empresa_distribuidora VARCHAR(20),
    no_empresa_distribuidora VARCHAR(200),
    no_cnpj VARCHAR(18),
    dt_atualizacao TIMESTAMP
);

COMMENT ON COLUMN dw.d_empresa_distribuidora.sk_empresa_distribuidora IS 'Chave primária da dimensão empresa distribuidora.';
COMMENT ON COLUMN dw.d_empresa_distribuidora.cd_empresa_distribuidora IS 'Sigla que abrevia o nome do Agente de Geração Distribuída. Mapeado de: SigAgente.';
COMMENT ON COLUMN dw.d_empresa_distribuidora.no_empresa_distribuidora IS 'Nome do Agente de Geração Distribuída. Mapeado de: NomAgente.';
COMMENT ON COLUMN dw.d_empresa_distribuidora.no_cnpj IS 'Cadastro Nacional de Pessoas Jurídicas da distribuidora. Mapeado de: NumCNPJDistribuidora.';
COMMENT ON COLUMN dw.d_empresa_distribuidora.dt_atualizacao IS 'Data da última atualização do registro.';

----------------------------------------------------------------------------------------------------

CREATE TABLE dw.d_cidade (
    sk_cidade INTEGER PRIMARY KEY,
    cd_cidade INTEGER,
    no_cidade VARCHAR(40),
    cd_estado VARCHAR(20),
    no_estado VARCHAR(50),
    no_regiao VARCHAR(50),
    vl_longitude DOUBLE PRECISION,
    vl_latitude DOUBLE PRECISION,
    dt_atualizacao TIMESTAMP
);

COMMENT ON COLUMN dw.d_cidade.sk_cidade IS 'Chave primária da dimensão de cidade.';
COMMENT ON COLUMN dw.d_cidade.cd_cidade IS 'Código do IBGE para o Município do empreendimento. Mapeado de: CodMunicipiolbge.';
COMMENT ON COLUMN dw.d_cidade.no_cidade IS 'Nome do Município do empreendimento. Mapeado de: NomMunicipio.';
COMMENT ON COLUMN dw.d_cidade.cd_estado IS 'Código do IBGE para a Unidade de Federação (UF). Mapeado de: codUFibge.';
COMMENT ON COLUMN dw.d_cidade.no_estado IS 'Sigla da Unidade de Federação (UF). Mapeado de: SigUF.';
COMMENT ON COLUMN dw.d_cidade.no_regiao IS 'Nome da Meso Região do empreendimento. Mapeado de: NomRegiao.';
COMMENT ON COLUMN dw.d_cidade.vl_longitude IS 'Longitude aproximada em grau decimal do empreendimento. Mapeado de: NumCoordEEmpreendimento.';
COMMENT ON COLUMN dw.d_cidade.vl_latitude IS 'Latitude aproximada em grau decimal do empreendimento. Mapeado de: NumCoordNEmpreendimento.';
COMMENT ON COLUMN dw.d_cidade.dt_atualizacao IS 'Data da última atualização do registro.';

----------------------------------------------------------------------------------------------------

CREATE TABLE dw.d_geracao (
    sk_geracao INTEGER PRIMARY KEY,
    cd_tipo VARCHAR(20),
    ds_tipo VARCHAR(50),
    no_fonte VARCHAR(50),
    no_porte VARCHAR(20),
    dt_atualizacao TIMESTAMP
);

COMMENT ON COLUMN dw.d_geracao.sk_geracao IS 'Chave primária da dimensão de geração.';
COMMENT ON COLUMN dw.d_geracao.cd_tipo IS 'Abreviação do tipo de geração (UFV, EOL, etc.). Mapeado de: SigTipoGeracao.';
COMMENT ON COLUMN dw.d_geracao.ds_tipo IS 'Descrição do tipo de geração (Central Geradora Solar Fotovoltaica, etc.). Campo inferido de SigTipoGeracao.';
COMMENT ON COLUMN dw.d_geracao.no_fonte IS 'Descrição do combustível ou fonte primária de energia. Mapeado de: DscFonteGeracao.';
COMMENT ON COLUMN dw.d_geracao.no_porte IS 'Porte do empreendimento (Microgeração ou Minigeração). Mapeado de: DscPorte.';
COMMENT ON COLUMN dw.d_geracao.dt_atualizacao IS 'Data da última atualização do registro.';

----------------------------------------------------------------------------------------------------

CREATE TABLE dw.d_fabricante (
    sk_fabricante INTEGER PRIMARY KEY,
    no_fabricante VARCHAR(20),
    no_modelo VARCHAR(200),
    dt_atualizacao TIMESTAMP
);

COMMENT ON COLUMN dw.d_fabricante.sk_fabricante IS 'Chave primária da dimensão de fabricante.';
COMMENT ON COLUMN dw.d_fabricante.no_fabricante IS 'Nome do fabricante do equipamento.';
COMMENT ON COLUMN dw.d_fabricante.no_modelo IS 'Modelo específico do equipamento.';
COMMENT ON COLUMN dw.d_fabricante.dt_atualizacao IS 'Data da última atualização do registro.';

----------------------------------------------------------------------------------------------------

CREATE TABLE dw.d_competencia (
    sk_competencia INTEGER PRIMARY KEY,
    nu_competencia INTEGER,
    nu_ano INTEGER,
    nu_mes INTEGER,
    no_mes VARCHAR(50),
    dt_inicio_mes DATE,
    dt_fim_mes DATE,
    dt_referencia DATE,
    dt_atualizacao TIMESTAMP
);

----------------------------------------------------------------------------------------------------

CREATE TABLE dw.d_data (
    sk_data int4 NOT NULL,
    nu_dia int4,
    nu_mes int4,
    no_mes varchar(50),
    nu_ano int4,
    dt_completa date,
    dt_atualizacao timestamp,
    CONSTRAINT d_data_pkey PRIMARY KEY (sk_data)
);

----------------------------------------------------------------------------------------------------

CREATE TABLE dw.f_geracao_distribuida (
    sk_tipo_consumidor INTEGER NOT NULL,
    sk_grupo_tarifario INTEGER NOT NULL,
    sk_empresa_distribuidora INTEGER NOT NULL,
    sk_cidade INTEGER NOT NULL,
    sk_geracao INTEGER NOT NULL,
    sk_competencia_cadastro INTEGER NOT NULL,
    sk_competencia_instalacao INTEGER NOT NULL,
    vl_potencia_instalada DOUBLE PRECISION,
    qt_modulos INTEGER,
    qt_empreendimentos INTEGER,
    dt_atualizacao TIMESTAMP
);

drop database if exists test;
create database test;
CREATE TABLE test.`null_id`
(
    `dt`                 date        NOT NULL COMMENT '日期',
    `tbl`                varchar(50) NOT NULL COMMENT '表名',
    `col`                varchar(50) NOT NULL COMMENT '列名',
    `value`              int         DEFAULT NULL COMMENT '空ID个数',
    `value_min`          int         DEFAULT NULL COMMENT '下限',
    `value_max`          int         DEFAULT NULL COMMENT '上限',
    `notification_level` int         DEFAULT NULL COMMENT '警告级别',
    PRIMARY KEY (`dt`, `tbl`, `col`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8
    comment '空值指标表';

CREATE TABLE test.`duplicate`
(
    `dt`                 date        NOT NULL COMMENT '日期',
    `tbl`                varchar(50) NOT NULL COMMENT '表名',
    `col`                varchar(50) NOT NULL COMMENT '列名',
    `value`              int         DEFAULT NULL COMMENT '重复值个数',
    `value_min`          int         DEFAULT NULL COMMENT '下限',
    `value_max`          int         DEFAULT NULL COMMENT '上限',
    `notification_level` int         DEFAULT NULL COMMENT '警告级别',
    PRIMARY KEY (`dt`, `tbl`, `col`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8
    comment '重复值指标表';

CREATE TABLE test.`rng`
(
    `dt`                 date        NOT NULL COMMENT '日期',
    `tbl`                varchar(50) NOT NULL COMMENT '表名',
    `col`                varchar(50) NOT NULL COMMENT '列名',
    `value`              int         DEFAULT NULL COMMENT '超出预定值域个数',
    `range_min`          int         DEFAULT NULL COMMENT '值域下限',
    `range_max`          int         DEFAULT NULL COMMENT '值域上限',
    `value_min`          int         DEFAULT NULL COMMENT '下限',
    `value_max`          int         DEFAULT NULL COMMENT '上限',
    `notification_level` int         DEFAULT NULL COMMENT '警告级别',
    PRIMARY KEY (`dt`, `tbl`, `col`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8
    comment '值域指标表';

CREATE TABLE test.`day_on_day`
(
    `dt`                 date        NOT NULL COMMENT '日期',
    `tbl`                varchar(50) NOT NULL COMMENT '表名',
    `value`              double DEFAULT NULL COMMENT '同比增长百分比',
    `value_min`          double DEFAULT NULL COMMENT '增长上限',
    `value_max`          double DEFAULT NULL COMMENT '增长上限',
    `notification_level` int    DEFAULT NULL COMMENT '警告级别',
    PRIMARY KEY (`dt`, `tbl`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8
    comment '环比增长指标表';

CREATE TABLE test.`week_on_week`
(
    `dt`                 date        NOT NULL COMMENT '日期',
    `tbl`                varchar(50) NOT NULL COMMENT '表名',
    `value`              double DEFAULT NULL COMMENT '环比增长百分比',
    `value_min`          double DEFAULT NULL COMMENT '增长上限',
    `value_max`          double DEFAULT NULL COMMENT '增长上限',
    `notification_level` int    DEFAULT NULL COMMENT '警告级别',
    PRIMARY KEY (`dt`, `tbl`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8
    comment '同比增长指标表';

CREATE TABLE test.`std_dev`
(
    `dt`                 date        NOT NULL COMMENT '日期',
    `tbl`                varchar(50) NOT NULL COMMENT '表名',
    `col`                varchar(50) NOT NULL COMMENT '列名',
    `value`              double DEFAULT NULL COMMENT '标准差',
    `value_min`          double DEFAULT NULL COMMENT '标准差上限',
    `value_max`          double DEFAULT NULL COMMENT '标准差上限',
    `notification_level` int    DEFAULT NULL COMMENT '警告级别',
    PRIMARY KEY (`dt`, `tbl`, `col`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8
    comment '标准差增长指标表';
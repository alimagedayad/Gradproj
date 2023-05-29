import { Button, Card, Col, Form, Row, Skeleton, Table, Typography } from 'antd';
import { green, red } from '@ant-design/colors';
import React, { useContext } from 'react';
import AddTransaction from './AddTransaction';
import EditableCell from './EditableCell';
import { EditingContext } from '../stores/EditingProvider';
import { HomeContext } from '../stores/HomeProvider';
import { TransactionsContext } from '../stores/TransactionsProvider';
import {
  UPDATE_TRANSACTIONS,
  EDIT_SELECTED,
  UPDATE_SELECTED,
  CANCEL_EDITING,
  HIDE_FOOTER,
  SHOW_FOOTER,
  ERROR,
} from '../../utils/misc/action-types';
import { columns, deleteTransactions, updateTransaction } from '../../utils/transactions/transactions';
import './ListOfTransactions.css';

const ListOfTransactions = ({ span, form, transactions }) => {
  const {
    state: transactionsState,
    dispatch: transactionsDispatch
  } = useContext(TransactionsContext);
  const {
    state: editingState,
    dispatch: editingDispatch
  } = useContext(EditingContext);
  const {
    state: homeState
  } = useContext(HomeContext);

  const cols = [
    {
      title: "Type",
      dataIndex: "type",
      key: "type",
    },
    {
      title: "Amount",
      dataIndex: "amount",
      key: "amount",
    },
    {
      title: "Merchant",
      dataIndex: "merchant",
      key: "merchant",
    },
    {
      title: "Category",
      dataIndex: "tran_category",
      key: "tran_category",
    },
    {
      title: "Bank",
      dataIndex: "bank",
      key: "bank",
    },
    {
      title: "Date",
      dataIndex: "date",
      key: "date",
    }
  ]

  cols[1].render = amount => {
    if (amount < 0) {
      return (
        <div style={{color: red[4]}}>
          - {(-amount).toFixed(2)} EGP
        </div>
      );
    } else {
      return (
        <div style={{color: green[3]}}>
          + {(+amount).toFixed(2)} EGP
        </div>
      );
    }

  }   

  const header = (
    <Row>
      <Col span={12} align="left">
        <Typography.Title level={2}>
          Transactions
        </Typography.Title>
      </Col>
      <Col span={12} align="right">
        <Typography.Text level={2}>
            Share Transactions
        </Typography.Text>
      </Col>
    </Row>
  );

  return (
    <Col {...span}>
      <Card className="transactions" title={header} bordered={false}>
            <Row>
                <Table
                  className="transactions"
                  columns={cols}
                  dataSource={transactions}
                  pagination={{ position: 'bottom' }}
                  size="middle"
                />
            </Row>
      </Card>
    </Col>
  );
};

export const EditableContext = React.createContext({});

export default ListOfTransactions;
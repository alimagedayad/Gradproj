import { Layout, Row, Button, Popconfirm, Space, Upload } from 'antd';

import React, {useState} from 'react';

import Breakdown from '../../components/charts/Breakdown';
import ListOfTransactions from '../../components/transactions/ListOfTransactions';
import { HomeProvider } from '../../components/stores/HomeProvider';
import { TransactionsProvider } from '../../components/stores/TransactionsProvider';
import '../root/Root.css';


const Home = () => {
  const [transactions, setTransactions] = useState([])

  const props = {
    name: 'file',
    accept: ".csv",
    action: 'http://127.0.0.1:5000/csv',
    onChange(info) {
    console.log("info: ", info)
    if (info.file.status !== 'uploading') {
      console.log(info.file, info.fileList);
    }
    if (info.file.status === 'done') {
      console.log(info.file.response);
      setTransactions(info.file.response)
    } else if (info.file.status === 'error') {
      console.log(info.file.response);
    }
  }
}

  const gutter = 16;
  return (
    <Layout id="home">
      <Layout.Content className="App">
        <HomeProvider>
          <TransactionsProvider>
            <Row type="flex" justify="center" gutter={gutter} >
              <Upload {...props}>
                <Button style={{
                  marginTop: '15px',
                }}>Upload your Bank Statement</Button>
              </Upload>
            </Row>
            
            <Row type="flex" justify="space-around">
              {/* <Expenses/> */}
              <Breakdown 
                transactions={transactions}
              />
            </Row>
            
            <Row type="flex" justify="space-around">
                <ListOfTransactions span={{ xs: 24 }} transactions={transactions} />
            </Row>
          </TransactionsProvider>
        </HomeProvider>
      </Layout.Content>
    </Layout>
  );
};

export default Home;
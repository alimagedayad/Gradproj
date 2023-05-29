import { Card, Col, Skeleton } from 'antd';
import React, { memo, useCallback, useContext, useEffect, useMemo, useState } from 'react';
import { Doughnut } from 'react-chartjs-2';

import ChartHeader from "./ChartHeader";
import { HomeContext } from '../stores/HomeProvider';
import { TransactionsContext } from '../stores/TransactionsProvider';
import { FINISHED_LOADING } from '../../utils/misc/action-types';
import { data, options, retrieveBreakdown } from '../../utils/charts/breakdown';
import './Breakdown.css';

const Breakdown = ({transactions}) => {
  const [chartType, setChartType] = useState('week');
  const [state, setState] =
    useState({
      weekBreakdown: [],
      weekLabels: [],
      monthBreakdown: [],
      monthLabels: [],
      yearBreakdown: [],
      yearLabels: [],
    });

  const { state: homeState, dispatch: homeDispatch } = useContext(HomeContext);
  const { state: transactionsState } = useContext(TransactionsContext);
 
  const handleClick = useCallback((e) => {
    e.preventDefault();
    const type = e.target.name;
    setChartType(type);
  }, [setChartType]);


  const [data, setData] = useState({
    labels: [],
    datasets: []
  })

  const categoryTotals = {}

  useEffect(() => {

    transactions.map((entry) => {
      const category = entry.tran_category;
      const amount = Math.abs(parseInt(entry.amount))

      if (category in categoryTotals) {
        categoryTotals[category] += amount
      } else {
        categoryTotals[category] = amount
      }
    })

    setData({
      labels: Object.keys(categoryTotals),
      datasets: [{
        label: "Breakdown",
        data: Object.values(categoryTotals),
        backgroundColor: [
          "#FF6384",
          "#36A2EB",
          "#FFCE56",
          "#81F4E1",
          "#36A2EB",
          "#3A4F41",
          "#E1DEE3",
          "#56CBF9",
          "#FFCE56",
          "#388659",
        ],
        borderColor: [
          "#FF6384",
          "#36A2EB",
          "#FFCE56",
          "#81F4E1",
          "#36A2EB",
          "#3A4F41",
          "#E1DEE3",
          "#56CBF9",
          "#FFCE56",
          "#388659",
        ],
      }]
    })

    console.log("data: ", data)

  }, [transactions])


  // const data = {
  //   labels: ['Food', 'Transportation', 'Entertainment', 'Other'],
  //   datasets: [{
  //     label: 'Breakdown',
  //     data: [300, 50, 100, 200],
  //   }]
  // }

  return (
    <Col {...{xs: 24, lg: 24}}>
      <Card
        className="doughnutChart"
        title={<ChartHeader title="Breakdown" onClick={handleClick} />}
        bordered={false}
      >
        { <Doughnut data={data} options={options} /> }
      </Card>
    </Col>
  );
};

export default memo(Breakdown);
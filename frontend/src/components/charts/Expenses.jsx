import { Card, Col, Skeleton } from 'antd';
import React, { memo, useCallback, useContext, useEffect, useMemo, useState } from 'react';
import { Line } from 'react-chartjs-2';

import ChartHeader from "./ChartHeader";
import { HomeContext } from '../stores/HomeProvider';
import {TransactionsContext} from '../stores/TransactionsProvider';
import { FINISHED_LOADING } from '../../utils/misc/action-types';
import { getDayLabels, getWeekLabels, getMonthLabels } from '../../utils/misc/date';
import { data, options, retrieveExpenses } from '../../utils/charts/expenses';
import './Expenses.css';

const Expenses = () => {
  const [chartType, setChartType] = useState('week');
  const [state, setState] =
    useState({
      weekExpenses: [],
      weekLabels: [],
      monthExpenses: [],
      monthLabels: [],
      yearExpenses: [],
      yearLabels: [],
    });

  // data for the current chart type
  const chartData = useMemo(() => {
    switch (chartType) {
      case 'week':
        return data(state.weekLabels, state.weekExpenses);
      case 'month':
        return data(state.monthLabels, state.monthExpenses);
      case 'year':
        return data(state.yearLabels, state.yearExpenses);
      default:
        return [];
    }
  }, [chartType, state]);

  // updates which chart is displayed
  const handleClick = useCallback((e) => {
    e.preventDefault();
    const type = e.target.name;
    setChartType(type);
  }, [setChartType]);

  return (
    <Col {...{xs: 24, lg: 24}}>
      <Card
        className="lineChart"
        title={<ChartHeader title="Expenses" onClick={handleClick} />}
        bordered={false}
      >
        <Line data={chartData} options={options} redraw/>
        {/* {homeState.isLoading
          ? <Skeleton active paragraph={{rows: 6}}/>
          : <Line data={chartData} options={options} redraw/>
        } */}
      </Card>
    </Col>
  );
};

export default memo(Expenses);
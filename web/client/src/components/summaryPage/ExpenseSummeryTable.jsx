import * as React from "react";
import {Table} from "antd";
import "./ExpenseSummeryTable.scss";
import axios from "axios";
import Text from "antd/es/typography/Text";


export default class ExpenseSummeryTable extends React.Component {

    tableColumns = [
        {
            title: 'Category Type',
            dataIndex: 'category_type',
            render: (value, row, index) => {
                const obj = {
                    children: value,
                    props: {},
                };
                if (!row.shouldRenderCategoryType) {
                    obj.props.rowSpan = 0;
                }
                else {
                    let count = 1;
                    for (let i = index; !this.state.expenses[i + 1].shouldRenderCategoryType; i++) {
                        count++ ;
                    }
                    obj.props.rowSpan = count;
                }
                return obj;
            },
            width: 100
        },
        {
            title: 'Category',
            dataIndex: 'category',
            width: 150
        },

        {
            title: 'Average',
            dataIndex: 'average'
        }];

    constructor(props) {
        super(props);
        this.state = {
            columns: this.tableColumns,
            expenses: null
        };
    }

    getColumns = () => {
        const months = [];
        const monthsColumns = [];
        let fromDate = this.props.fromDate.clone();
        let toDate = this.props.toDate.clone();
        while (fromDate.isBefore(toDate)) {
            months.push(fromDate.format("MM"));
            fromDate.add(1, 'month');
        }
        months.forEach(month => {
            monthsColumns.push({
                title: month,
                dataIndex: month,
            });
        });
        return [...this.tableColumns.slice(0, 2), ...monthsColumns, this.tableColumns.slice(-1)[0]]
    };

    componentDidMount = () => {
        this.getExpenseData();
    };

    componentDidUpdate = (prevProps) => {
        if (prevProps.fromDate !== this.props.fromDate || prevProps.toDate !== this.props.toDate) {
            this.getExpenseData();
        }
    };

    getExpenseData = () => {
        axios.get('/api/expense_summery', {
            params: {
                fromDate: this.props.fromDate.format("DD-MM-YYYY"),
                toDate: this.props.toDate.format("DD-MM-YYYY"),
                categoryTypes: JSON.stringify(this.props.categoryTypes)
            }
        })
            .then(res => {
                this.populateData(res.data);
            })
    };

    populateData = (expenseData) => {
        console.log(expenseData);
        const categoryTypes = new Set();

        expenseData.forEach((expense) => {
            expense.key = expense.category;  // because the category is different for every row
            if (!categoryTypes.has(expense.category_type)) {
                expense.shouldRenderCategoryType = true;
            }
            else {
                expense.shouldRenderCategoryType = false;
            }
            categoryTypes.add(expense.category_type);

        });

        this.setState({
            expenses: expenseData,
            columns: this.getColumns()
        });
    };


    render() {
        if (this.state.expenses == null) {
            return (<div></div>);
        }

        const lastRowData = this.state.expenses[this.state.expenses.length - 1];
        const rowCells = [];
        Object.keys(lastRowData).forEach(key => {
            rowCells.push(React.createElement('td', {key: key, className: 'ant-table-cell'}, lastRowData[key]));
        });
        const lastRow = React.createElement('tr', {className: 'summary-row'}, rowCells);
        console.log(lastRow);
        return (
            <div>
                <Table dataSource={this.state.expenses.slice(0, -1)} columns={this.state.columns}
                       rowClassName={(record, index) => record.amount > 0 ? "credit-row" : 'debit-row'}
                       pagination={false}
                       // scroll={{ y: 550 }}
                       size="small"
                       bordered
                       tableLayout={'auto'}
                       summary={pageData => {
                           return (
                               <>
                               {lastRow}
                               </>
                           );
                       }}
                />
            </div>
        );
    }
}
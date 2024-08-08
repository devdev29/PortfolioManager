import Chart from 'chart.js/auto';
import { Component, signal } from "@angular/core";
import { PortfolioCash } from 'src/model/portfolio-cash.model';
import { PortfolioStocks } from 'src/model/portfolio-stocks.model';
import { faWallet, faMoneyBillTrendUp } from '@fortawesome/free-solid-svg-icons';

@Component ({
    selector : 'app-asset',
    templateUrl : './asset.component.html',
    styleUrls : ['./asset.component.css']
})

export class AssetComponent { 
    public spendingChart: any;
    public incomeChart: any;
    public faWallet = faWallet;
    public faMoneyBillTrendUp = faMoneyBillTrendUp;
    readonly panelOpenState = signal(false);
    public cashComponents: PortfolioCash[] = [
        {
            accountNumber: 'XXXX',
            bankName: 'SBI',
            balance: 15000,
            accountType: 'savings'
        },
        {
            accountNumber: 'XXXX',
            bankName: 'Yes Bank',
            balance: 15000,
            accountType: 'savings'
        }
    ];
    public stockComponents: PortfolioStocks[] = [
        {
            ticker: 'AAPL',
            full_name: 'Apple Inc',
            quantity: 100,
            market_cap: 'large',
            exchange: 'NYSE',
            account_no: 'aaa',
            amount_invested: 20700.00
        },
        {
            account_no: "bbb",
            amount_invested: 40000.0,
            exchange: "NYSE",
            full_name: "Microsoft Corp",
            market_cap: "large",
            quantity: 100,
            ticker: "MSFT"
        }
    ];

    ngOnInit(): void {
        // this.createSpendingChart();
        // this.createIncomeChart();
    }

    // createIncomeChart(): void {
    //     this.incomeChart = new Chart("incomeChart", {
    //         type: 'doughnut', 
    //         data: {
    //             labels: [ 'Wheat', 'Maize', 'Rice', 'Sugarcane', 'Cotton' ], 
	//             datasets: [
    //                 { 
    //                     label: 'Income', 
    //                     data: [9168.2, 1417.8, 3335.1, 1165.0, 2078.9],
    //                     backgroundColor: ['#4e79a7', '#59a14f', '#f28e2c', '#e15759', '#b07aa1'],
    //                     borderColor: ['transparent', 'transparent', 'transparent', 'transparent', 'transparent'],
    //                     borderWidth: [1, 1, 1, 1, 1],
    //                     hoverOffset: 4
    //                 }
    //             ]
    //         },
    //         options: { 
    //             aspectRatio: 2.5,
    //             plugins: {
    //                 title: {
    //                     display: true,
    //                     text: 'Income $42,000',
    //                     font: { size: 24, weight: 'bold', family: "sans-serif" },
    //                     color: 'white',
    //                     padding: { top: 10, bottom: 30 }
    //                 },
    //                 legend: {  
    //                     display: false
    //                 }
    //             }
    //         }
    //     });
    // }

    // createSpendingChart(): void {
    //     this.spendingChart = new Chart("spendingChart", {
    //         type: 'doughnut', 
    //         data: {
    //             labels: [ 'Wheat', 'Maize', 'Rice', 'Sugarcane', 'Cotton' ], 
	//             datasets: [
    //                 { 
    //                     label: 'Area and Production of Important Crops (2020-21)', 
    //                     data: [9168.2, 1417.8, 3335.1, 1165.0, 2078.9],
    //                     backgroundColor: ['rgb(255, 99, 132)', 'rgb(54, 162, 235)', 'rgb(255, 205, 86)', 'rgb(75, 192, 192)', 'rgb(153, 102, 255)'],
    //                     hoverOffset: 4
    //                 }
    //             ]
    //         },
    //         options: { 
    //             aspectRatio: 2.5,
    //             plugins: {
    //                 title: {
    //                     display: true,
    //                     text: 'Area and Production of Important Crops (2020-21)',
    //                     font: { size: 24, weight: 'bold', family: "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif" },
    //                     color: 'white',
    //                     padding: { top: 10, bottom: 30 }
    //                 },
    //                 legend: {  
    //                     display: true,
    //                     labels: {
    //                         font: { size: 14, family: "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif" },
    //                         color: 'white'
    //                     }
    //                 }
    //             }
    //         }
    //     });
    // }

    buyStocks(i: number, stockCount: string): void {
        const count = Number(stockCount);
        if (!isNaN(count)) {
            console.log(`Buying ${count} stocks of ${this.stockComponents[i].full_name}`);
        } else {
            console.error('Invalid input for stock count');
        }
    }

    sellStocks(i: number, stockCount: string): void {
        const count = Number(stockCount);
        if (!isNaN(count)) {
            console.log(`Selling ${count} stocks of ${this.stockComponents[i].full_name}`);
        } else {
            console.error('Invalid input for stock count');
        }
    }
}

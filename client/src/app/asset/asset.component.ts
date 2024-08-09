import Chart from 'chart.js/auto';
import { Component, signal } from "@angular/core";
import { PortfolioCash } from 'src/model/portfolio-cash.model';
import { PortfolioStocks } from 'src/model/portfolio-stocks.model';
import { faWallet, faMoneyBillTrendUp } from '@fortawesome/free-solid-svg-icons';
import { HttpClient } from '@angular/common/http';
import { catchError, Observable, throwError } from 'rxjs';
import { AppComponent } from '../app.component';
import { AppRoutingModule } from '../app-routing.module';
import { Router } from '@angular/router';

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

    public cashComponents: PortfolioCash[] = [];
    public stockComponents: PortfolioStocks[] = [];

    constructor(private http: HttpClient, private app: AppComponent, private router: Router) { }

    errorHandler(error: {
        error: { message: string; };
        status: any; message: any;
    }) {
        let errorMessage = '';
        if (error.error instanceof ErrorEvent) {
            errorMessage = error.error.message;
        } 
        else {
            errorMessage = `Error Code: ${error.status}\nMessage: ${error.message}`;
        }
        return throwError(errorMessage);
    }

    getStocks(): Observable<any> {
        return this.http.get(this.app.domain + 'stocks/portfolio/all').pipe(catchError(this.errorHandler));
    }

    getCash(): Observable<any> {
        return this.http.get(this.app.domain + 'accounts/all').pipe(catchError(this.errorHandler));
    }

    updateStock(body: any): Observable<any> {
        return this.http.put(this.app.domain + 'stocks/portfolio', body).pipe(catchError(this.errorHandler));
    }

    deleteStock(ticker: string): Observable<any> {
        return this.http.delete(this.app.domain + 'stocks/portfolio/' + ticker).pipe(catchError(this.errorHandler));
    }

    ngOnInit(): void {
        this.getCash().subscribe(data => {
            console.log(data);
            this.cashComponents = data;
        });

        this.getStocks().subscribe(data => {
            console.log(data);
            this.stockComponents = data;
        });
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
            var final_qty = this.stockComponents[i].quantity + count;
            var body = {
                'ticker': this.stockComponents[i].ticker,
                'quantity': final_qty
            };
            this.updateStock(body).subscribe(data => {
                console.log(data);
                window.location.reload();
            });
        } 
        else {
            console.error('Invalid input for stock count');
        }
    }

    sellStocks(i: number, stockCount: string): void {
        const count = Number(stockCount);
        if (!isNaN(count) && count < this.stockComponents[i].quantity) {
            console.log(`Selling ${count} stocks of ${this.stockComponents[i].full_name}`);
            var final_qty = this.stockComponents[i].quantity - count;
            var body = {
                'ticker': this.stockComponents[i].ticker,
                'quantity': final_qty
            };
            this.updateStock(body).subscribe(data => {
                console.log(data);
                window.location.reload();
            });
        }
        else if (!isNaN(count) && count == this.stockComponents[i].quantity) {
            console.log(`Got to close this account of ${this.stockComponents[i].full_name}`);
            this.deleteStock(this.stockComponents[i].ticker).subscribe(data => {
                console.log(data);
                window.location.reload();
            });
        }
        else {
            console.error('Invalid input for stock count');
        }
    }
}

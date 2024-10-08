import { Component, Injectable, signal } from "@angular/core";
import { PortfolioCash } from 'src/model/portfolio-cash.model';
import { PortfolioStocks } from 'src/model/portfolio-stocks.model';
import { faWallet, faMoneyBillTrendUp, faHandHoldingDollar, faHand } from '@fortawesome/free-solid-svg-icons';
import { HttpClient } from '@angular/common/http';
import { catchError, Observable, throwError } from 'rxjs';
import { AppComponent } from '../app.component';
import { Router } from '@angular/router';
import { PortfolioMutualFunds } from 'src/model/portfolio-mf.model';

@Component ({
    selector : 'app-asset',
    templateUrl : './asset.component.html',
    styleUrls : ['./asset.component.css']
})

@Injectable({
    providedIn: 'root'
})

export class AssetComponent { 
    public spendingChart: any;
    public incomeChart: any;
    public faWallet = faWallet;
    public faMoneyBillTrendUp = faMoneyBillTrendUp;
    public faHandHoldingDollar = faHandHoldingDollar;
    readonly panelOpenState = signal(false);

    public cashComponents: PortfolioCash[] = [];

    public stockComponents: PortfolioStocks[] = [];

    public mfComponents: PortfolioMutualFunds[] = [];

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

    getCash(): Observable<any> {
        return this.http.get(this.app.domain + 'accounts/all').pipe(catchError(this.errorHandler));
    }

    getFunds(): Observable<any> {
        return this.http.get(this.app.domain + 'mutual_funds/portfolio/all').pipe(catchError(this.errorHandler));
    }

    getStocks(): Observable<any> {
        return this.http.get(this.app.domain + 'stocks/portfolio/all').pipe(catchError(this.errorHandler));
    }

    updateStock(body: any): Observable<any> {
        return this.http.put(this.app.domain + 'stocks/portfolio', body).pipe(catchError(this.errorHandler));
    }

    updateFunds(body: any): Observable<any> {
        return this.http.put(this.app.domain + 'mutual_funds/portfolio', body).pipe(catchError(this.errorHandler));
    }

    deleteStock(ticker: string): Observable<any> {
        return this.http.delete(this.app.domain + 'stocks/portfolio/' + ticker).pipe(catchError(this.errorHandler));
    }

    deleteFunds(mf_id: string): Observable<any> {
        return this.http.delete(this.app.domain + 'stocks/portfolio/' + mf_id).pipe(catchError(this.errorHandler));
    }


    ngOnInit(): void {
        this.getCash().subscribe(data => {
            console.log(JSON.stringify(data));
            this.cashComponents = data;
        });

        this.getStocks().subscribe(data => {
            console.log(JSON.stringify(data));
            this.stockComponents = data;
        });

        this.getFunds().subscribe(data => {
            console.log(JSON.stringify(data));
            this.mfComponents = data;
        });
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

    sellFunds(i: number, fundCount: string): void {
        const count = Number(fundCount);
        if (!isNaN(count) && count < this.mfComponents[i].quantity) {
            console.log(`Selling ${count} mutual funds of ${this.mfComponents[i].name}`);
            var final_qty = this.mfComponents[i].quantity - count;
            var body = {
                'mf_id': this.mfComponents[i].mf_id,
                'quantity': final_qty
            };
            this.updateFunds(body).subscribe(data => {
                console.log(data);
                window.location.reload();
            });
        }
        else if (!isNaN(count) && count == this.stockComponents[i].quantity) {
            console.log(`Got to close this account of ${this.mfComponents[i].name}`);
            this.deleteFunds(this.mfComponents[i].mf_id.toString()).subscribe(data => {
                console.log(data);
                window.location.reload();
            });
        }
        else {
            console.error('Invalid input for mutual funds count');
        }
    }

    buyFunds(i: number, fundCount: string): void {
        const count = Number(fundCount);
        if (!isNaN(count)) {
            console.log(`Buying ${count} mutual funds of ${this.stockComponents[i].full_name}`);
            var final_qty = this.mfComponents[i].quantity - count;
            var body = {
                'mf_id': this.mfComponents[i].mf_id,
                'quantity': final_qty
            };
            this.updateFunds(body).subscribe(data => {
                console.log(data);
                window.location.reload();
            });
        } 
        else {
            console.error('Invalid input for stock count');
        }
    }
}

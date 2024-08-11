import { HttpClient } from "@angular/common/http";
import { Component, Injectable, signal } from "@angular/core";
import { AppComponent } from "../app.component";
import { Router } from "@angular/router";
import { catchError, Observable, throwError } from "rxjs";
import { PortfolioCash } from "src/model/portfolio-cash.model";

@Component ({
    selector : 'app-add-asset',
    templateUrl : './add-asset.component.html',
    styleUrls : ['./add-asset.component.css']
})

@Injectable({
    providedIn: 'root'
})

export class AddAssetComponent {

    public ticker: string = '';
    public stock_account_no: string = '';
    public stock_quantity: number = 0;
    public stock_full_name: string = '';
    public stock_exchange: string = '';
    public stock_mcap: string = 'medium';
    public tickerOptions: any[] = [];
    public stock_price: number = 0;
    
    // public mf_id: number = 0;
    // public mf_name: string = '';
    // public mf_quantity: number = 0;
    // public mf_account_no: string = '';
    // public mfOptions: any[] = [];
    
    public active_tab: number = 1;
    public accountList: PortfolioCash[] = [];


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

    getStockByTicker(ticker: string): Observable<any> {
        return this.http.get(this.app.domain + 'stocks/search/' + ticker).pipe(catchError(this.errorHandler));
    }

    addStock(body: any): Observable<any> {
        return this.http.post(this.app.domain + 'stocks/portfolio', body).pipe(catchError(this.errorHandler));
    }

    getStockPrice(ticker: string): Observable<any> {
        return this.http.get('https://financialmodelingprep.com/api/v3/quote-short/' + ticker + '?apikey=P9kDMRB0vVROszNoKmbYfW9VvEVUk222').pipe(catchError(this.errorHandler));
    }

    ngOnInit() {
        this.getCash().subscribe(data => {
            console.log(JSON.stringify(data));
            this.accountList = data;
        });
    }

    searchTicker() {
        this.tickerOptions =[];
        if(this.ticker.length === 0 || this.ticker.length === 1 || this.ticker.length === 2)
            return;
        this.getStockByTicker(this.ticker.toUpperCase()).subscribe(data => {
            console.log(JSON.stringify(data));
            this.tickerOptions = data;
        });
    }

    // searchMF() {
    //     this.mfOptions =[];
    //     if(this.ticker.length === 0 || this.ticker.length === 1 || this.ticker.length === 2)
    //         return;
    //     this.getStockByTicker(this.ticker.toUpperCase()).subscribe(data => {
    //         console.log(JSON.stringify(data));
    //         this.tickerOptions = data;
    //     });
    //     console.log(this.ticker);
    // }



    selectTicker(i: number) {
        this.ticker = this.tickerOptions[i].symbol;
        this.stock_full_name = this.tickerOptions[i].name;
        this.stock_exchange = this.tickerOptions[i].exchangeShortName;
        this.tickerOptions = [];
        this.getStockPrice(this.ticker).subscribe(data => {
            console.log(JSON.stringify(data));
            this.stock_price = data[0].price;
        });
    }

    // selectMF(i: number) {
    //     this.ticker = this.tickerOptions[i].symbol;
    //     this.stock_full_name = this.tickerOptions[i].name;
    //     this.stock_exchange = this.tickerOptions[i].exchangeShortName;
    //     this.tickerOptions = [];
    // }

    fixAccountforStocks(event: any) {
        this.stock_account_no = event.target.value;
        console.log('Selected account:', this.stock_account_no);
    }

    // fixAccountforMF(event: any) {
    //     this.mf_account_no = event.target.value;
    //     console.log('Selected account:', this.mf_account_no);
    // }

    addStocks() {
        var body = {
            "ticker": this.ticker,
            "quantity": this.stock_quantity,
            "account_no": this.stock_account_no,
            "exchange": this.stock_exchange,
            "market_cap": this.stock_mcap,
            "full_name": this.stock_full_name
        };
        console.log(body);
        this.addStock(body).subscribe(data => {
            console.log(JSON.stringify(data));
            window.location.reload();
        });
    }

    // addMF() {
    //     var body = {
    //         "ticker": this.ticker,
    //         "quantity": this.stock_quantity,
    //         "account_no": this.stock_account_no,
    //         "exchange": this.stock_exchange,
    //         "market_cap": this.stock_mcap,
    //         "full_name": this.stock_full_name
    //     };
    //     console.log(body);
    //     this.addStock(body).subscribe(data => {
    //         console.log(JSON.stringify(data));
    //         window.location.reload();
    //     });
    // }

    selectTab(val: number) {
        this.active_tab = val;
    }
}
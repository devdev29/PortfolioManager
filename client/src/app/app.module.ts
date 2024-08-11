import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from "@angular/common/http";
import { MatButtonToggleModule } from '@angular/material/button-toggle'
import { AppComponent } from './app.component';
import { MenuComponent } from './menu/menu.component';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { DashboardComponent } from './dashboard/dashboard.component';
import { AssetComponent } from './asset/asset.component';
import { HeaderComponent } from './header/header.component';
import { AddAssetComponent } from './add-asset/add-asset.component';
import { TransactionComponent } from './transaction/transaction.component';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatInputModule } from '@angular/material/input';
import { MatNativeDateModule } from '@angular/material/core';
import { MatFormFieldModule } from '@angular/material/form-field';
import { DatePipe } from '@angular/common';

@NgModule({
  declarations: [
    AppComponent,
    MenuComponent,
    HeaderComponent,
    DashboardComponent,
    AssetComponent,
    AddAssetComponent,
    TransactionComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule,
    AppRoutingModule,
    FontAwesomeModule,
    MatButtonToggleModule,
    BrowserAnimationsModule,
    MatDatepickerModule,
    MatInputModule,
    MatFormFieldModule, 
    MatNativeDateModule
  ],
  providers: [DatePipe], 
  bootstrap: [AppComponent]
})
export class AppModule { }

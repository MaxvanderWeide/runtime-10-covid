import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import {EnvServiceProvider} from "./services/env.service.provider";
import {HttpClientModule} from "@angular/common/http";
import {HeaderComponent} from "./components/header/header.component";

@NgModule({
    declarations: [
        AppComponent,
        HeaderComponent
    ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [EnvServiceProvider],
  bootstrap: [AppComponent]
})
export class AppModule { }

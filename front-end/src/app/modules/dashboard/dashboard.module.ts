import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DashboardComponent } from './dashboard.component';
import {AppModule} from "../../app.module";
import {HeaderComponent} from "../../components/header/header.component";



@NgModule({
  declarations: [
    DashboardComponent,
    HeaderComponent
  ],
  exports: [
    DashboardComponent
  ],
  imports: [
    CommonModule
  ]
})
export class DashboardModule { }

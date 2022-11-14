import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {DashboardComponent} from "./modules/dashboard/dashboard.component";
import {PolicyComponent} from "./modules/policy/policy.component";
import {ReadmeComponent} from "./modules/readme/readme.component";

const routes: Routes = [
  { path: '', component: DashboardComponent },
  { path: 'policy', component: PolicyComponent},
  { path: 'readme', component: ReadmeComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

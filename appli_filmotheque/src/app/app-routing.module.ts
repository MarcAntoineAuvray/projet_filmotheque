import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DashboardComponent } from './dashboard/dashboard.component';
import { LoginComponent } from './login/login.component';
import { SingupComponent } from './signup/singup.component';

const routes: Routes = [
  {redirectTo:'', path:'login', pathMatch:'full'},
  {path:'login',component:LoginComponent},
  {path:'singup',component:SingupComponent},
  {path:'dashboard',component:DashboardComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

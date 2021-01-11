import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Routes, RouterModule } from '@angular/router';
import { DashboardComponent } from './dashboard/dashboard.component';
import { TicketsComponent } from './tickets/tickets.component';
import { LoginComponent } from './login/login.component';
import { TicketdetailComponent } from './ticketdetail/ticketdetail.component';
import { AddticketComponent } from './addticket/addticket.component';

const routes: Routes = [
  {
    path: '',
    redirectTo: '/login',
    pathMatch: 'full'
  },
  {
    path: 'login',
    component: LoginComponent
  },
  {
    path: 'dashboard',
    component: DashboardComponent
  },
  {
    path: 'addticket',
    component: AddticketComponent
  },
  {
    path: 'tickets',
    component: TicketsComponent
  },
  {
    path: 'tickets/:ticketID',
    component: TicketdetailComponent
  }
];

@NgModule({
  imports: [CommonModule, RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

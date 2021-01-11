import { Component, OnInit } from '@angular/core';
import {MatTableDataSource} from '@angular/material/table';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';

import { environment } from "../../environments/environment";


@Component({
  selector: 'app-tickets',
  templateUrl: './tickets.component.html',
  styleUrls: ['./tickets.component.css']
})

export class TicketsComponent implements OnInit {
  displayedColumns: string[] = ['sino', 'date', 'state', 'jiraID', 'title', 'module', '_id'];
  tickets: TicketData[] = [];

  dataSource: any;

  searchParams: { [char: string]: string } = {
    jid: '',
    sts: '',
    fdt: '',
    tdt: '',
  }

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private http: HttpClient
  ) {}


  ngOnInit() {
    this.route.queryParams.subscribe((params) => {
      this.searchParams = {...this.searchParams, ...params};
    });
    this.getTickets();
  }

  getTickets() {

    let qstr = [];
    let qstring = '';
    for (const k in this.searchParams) {
      if (this.searchParams[k] != '') {
        const encodedVal = encodeURIComponent(this.searchParams[k]);
        qstr[qstr.length] = `${k}=${encodedVal}`;
      }
    }
    if (qstr.length) {
      qstring = qstr.join('&');
    }

    this.http.get(`${environment.serviceUrl}api/tickets?${qstring}`).subscribe((res: any) => {
      if (res.error.status) {
        this.dataSource = new MatTableDataSource<TicketData>(res.payload);
      }
    });
  }

  onClickSearch() {
    this.getTickets()
  }

  onClickViewDetails(_id: number) {
    this.router.navigate(['/tickets/', _id]);
  }

  onClickAdd() {
    this.router.navigate(['/addticket']);
  }

}

export interface TicketData {
  _id: number,
  sino: number;
  date: string;
  state: string;
  jiraID: string;
  title: string;
  module: string;
  team?:number;
}


export interface TicketResponse {
  error: {
    status: number;
  },
  auth: {},
  payload: [ TicketData ]
}

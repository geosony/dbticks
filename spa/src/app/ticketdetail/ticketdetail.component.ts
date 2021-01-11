import { Component, Inject, OnInit } from '@angular/core';
import { MatBottomSheet, MatBottomSheetRef, MAT_BOTTOM_SHEET_DATA } from '@angular/material/bottom-sheet';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { environment } from "../../environments/environment";


@Component({
  selector: 'app-ticketdetail',
  templateUrl: './ticketdetail.component.html',
  styleUrls: ['./ticketdetail.component.css']
})
export class TicketdetailComponent implements OnInit {

  viewonly:boolean = true
  isLoading:boolean = false
  ticketID:string = '';

  ticket: any = {
    jiraID: 'SUPPORT-1234',
    reportedDate: '05-12-2020',
    status: '1',
    team: '2',
    title: 'Ticket Title',
    module: 'Module::__METHOD__'
  };

  query: any = {
    fullQuery: `SELECT id FROM table_nothing WHERE 1=1`,

    title: 'Give some identifier title to identify this query later.',
    fix: 'Paste your solution/fix or comments here..',
    time: '',
    dbName: '',
    host: '',
    ip: '',
    execTime: 0,
    lockTime: 0,
    rowsSent: 0,
    rowsExamined:0
  };

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private http: HttpClient,
    private _bottomSheet: MatBottomSheet) {}

  ngOnInit() {
    this.route.params.subscribe(
      (params:Params) => {
        this.getTicketDetail(params.ticketID);
      }
    );
  }


  getTicketDetail(ticketID: string) {
    this.ticketID = ticketID;
    this.http.get(`${environment.serviceUrl}api/tickets/${ticketID}/detail`).subscribe((res: any) => {
      if (res.error.status) {
        const payload = res.payload[0];
        this.ticket.jiraID = payload.ticket.jiraID;
        this.ticket.reportedDate = payload.ticket.dateStr;
        this.ticket.status = payload.ticket.status;
        this.ticket.team = payload.ticket.team;
        this.ticket.title = payload.ticket.title;
        this.ticket.module = payload.ticket.module;

        this.query.title = payload.querytitle || '';
        this.query.fix = payload.queryfix || '';

        this.query.time = payload.datetime.date + ' ' + payload.datetime.time;
        this.query.dbName = payload.db.name;
        this.query.host = payload.host.host;
        this.query.ip = payload.host.ip;
        this.query.execTime = payload.analytics.query_time;
        this.query.lockTime = payload.analytics.lock_time;
        this.query.rowsSent = payload.analytics.rows_sent;
        this.query.rowsExamined = payload.analytics.rows_examined;
        const regex = /[\s]+/g;
        this.query.fullQuery = payload.query.replace(regex, " ");
        this.query.halfQuery = this.query.fullQuery.substring(0, 160) + '...';
      }
    });
  }
  onClickBack(page: string) {
    this.router.navigate(['/' + page])
  }

  onClickEdit() {
    this.viewonly = false;
  }
  onClickSave() {

    const formData = new FormData();

    formData.append("title", this.ticket.title);
    const postData = {
      "title": this.ticket.title,
      "jiraID": this.ticket.jiraID,
      "repDate": this.ticket.reportedDate,
      "status": this.ticket.status,
      "module": this.ticket.module,
      "team": this.ticket.team,
      "qtitle": this.query.title,
      "qfix": this.query.fix,
    };

    const ticketID = this.ticketID;

    this.http.post(`${environment.serviceUrl}api/tickets/${ticketID}/update`, postData).subscribe((res: any) => {
      console.log(res);
    });
    this.viewonly = true;
  }


  onClickCompare(): void {
    this.isLoading = true;
    const ticketID = this.ticketID;
    this.http.get(`${environment.serviceUrl}api/tickets/${ticketID}/compare`).subscribe((res: any) => {
      if (res.error.status) {
        const payload = res.payload;
        this.isLoading = false;
        this._bottomSheet.open(TicketsComparison, { data: payload });
      }
    });
  }
}

@Component({
  selector: 'ticket-comparison',
  templateUrl: 'ticket-comparison.html',
  styleUrls: ['./ticketdetail.component.css']
})
export class TicketsComparison {

  comparisonData: any = [];

  constructor(
    @Inject(MAT_BOTTOM_SHEET_DATA) public data: any,
    private _bottomSheetRef: MatBottomSheetRef<TicketsComparison>,
    private router: Router,
  ) {
    this.comparisonData = data;
  }

  onClickID(event: MouseEvent, _id: string): void {
    this.router.navigate(['/tickets' + _id]);
    this._bottomSheetRef.dismiss();
    event.preventDefault();
  }


}

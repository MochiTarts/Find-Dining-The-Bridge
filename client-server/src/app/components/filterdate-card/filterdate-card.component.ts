import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-filterdate-card',
  templateUrl: './filterdate-card.component.html',
  styleUrls: ['./filterdate-card.component.scss']
})
export class FilterdateCardComponent implements OnInit {

  @Input() months: string[];
  @Input() years: string[];
  @Input() monthsLength: number;
  @Input() yearsLength: number;

  @Output() monthEvents: EventEmitter<any> = new EventEmitter<any>();
  @Output() yearEvents: EventEmitter<any> = new EventEmitter<any>();

  monthCheckMap: boolean[] = new Array(length);
  yearCheckMap: boolean[] = new Array(length);

  constructor() {}

  ngOnInit(): void {
    for (let i = 0; i < this.monthsLength; i++) {
      this.monthCheckMap.push(false);
    }

    for (let i = 0; i < this.yearsLength; i++) {
      this.yearCheckMap.push(false);
    }
  }

  selectAll() {
    this.monthCheckMap = [];
    this.yearCheckMap = [];
    var inputs = document.getElementsByTagName("input");
    for (var i = 0; i < inputs.length; i++) { 
        if (inputs[i].type == "checkbox") { 
            inputs[i].checked = true;
        }
        if (inputs[i].name == "months") {
          this.monthCheckMap.push(true);
        }
        if (inputs[i].name == "years") {
          this.yearCheckMap.push(true);
        }
    }
  }

  reset() {
    this.monthCheckMap = [];
    this.yearCheckMap = [];
    var inputs = document.getElementsByTagName("input");
    for (var i = 0; i < inputs.length; i++) { 
        if (inputs[i].type == "checkbox") { 
            inputs[i].checked = false;
        }
        if (inputs[i].name == "months") {
          this.monthCheckMap.push(false);
        }
        if (inputs[i].name == "years") {
          this.yearCheckMap.push(false);
        }
    }
  }

  sendList() {
    this.monthEvents.emit(this.monthCheckMap);
    this.yearEvents.emit(this.yearCheckMap);
  }

}

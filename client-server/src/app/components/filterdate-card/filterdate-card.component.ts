import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-filterdate-card',
  templateUrl: './filterdate-card.component.html',
  styleUrls: ['./filterdate-card.component.scss']
})
export class FilterdateCardComponent implements OnInit {

  @Input() months: string[];
  @Input() years: string[];

  @Output() events: EventEmitter<any> = new EventEmitter<any>();

  monthCheckMap: boolean[] = new Array(length);
  yearCheckMap: boolean[] = new Array(length);

  constructor() {}

  ngOnInit(): void {
    for (let i = 0; i < 12; i++) {
      this.monthCheckMap.push(false);
    }

    for (let i = 0; i < 6; i++) {
      this.yearCheckMap.push(false);
    }
  }

  /**
   * Selects all the months and years and sets the
   * monthCheckMap and yearCheckMap to all true
   */
  selectAll() {
    this.monthCheckMap = [];
    this.yearCheckMap = [];
    var inputs = document.getElementsByTagName("input");
    for (var i = 0; i < inputs.length; i++) { 
        if (inputs[i].type == "checkbox") { 
            inputs[i].checked = true;
        }
    }

    for (let i = 0; i < 12; i++) {
      this.monthCheckMap.push(true);
    }

    for (let i = 0; i < 6; i++) {
      this.yearCheckMap.push(true);
    }
  }

  /**
   * Deselects all the months and years and sets the
   * monthCheckMap and yearCheckMap to all false
   */
  reset() {
    this.monthCheckMap = [];
    this.yearCheckMap = [];
    var inputs = document.getElementsByTagName("input");
    for (var i = 0; i < inputs.length; i++) { 
        if (inputs[i].type == "checkbox") { 
            inputs[i].checked = false;
        }
    }

    for (let i = 0; i < 12; i++) {
      this.monthCheckMap.push(false);
    }

    for (let i = 0; i < 6; i++) {
      this.yearCheckMap.push(false);
    }
  }

  /**
   * Emits the monthCheckMap and yearCheckMap to be used
   * in articles page for filtering
   */
  sendList() {
    var checkMap = {
      month: this.monthCheckMap,
      year: this.yearCheckMap
    }
    this.events.emit(checkMap);
  }

}

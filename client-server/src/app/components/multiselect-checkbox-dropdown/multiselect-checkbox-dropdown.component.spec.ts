import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MultiselectCheckboxDropdownComponent } from './multiselect-checkbox-dropdown.component';

describe('MultiselectCheckboxDropdownComponent', () => {
  let component: MultiselectCheckboxDropdownComponent;
  let fixture: ComponentFixture<MultiselectCheckboxDropdownComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ MultiselectCheckboxDropdownComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MultiselectCheckboxDropdownComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

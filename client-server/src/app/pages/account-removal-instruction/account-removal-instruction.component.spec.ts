import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AccountRemovalInstructionComponent } from './account-removal-instruction.component';

describe('AccountRemovalInstructionComponent', () => {
  let component: AccountRemovalInstructionComponent;
  let fixture: ComponentFixture<AccountRemovalInstructionComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AccountRemovalInstructionComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AccountRemovalInstructionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

import pytest
from polyforms.perfect_seq import *


@pytest.fixture(autouse=True)
def setup_teardown():
    # Setup code
    seq_storage = PerfectSeq()
    yield seq_storage  # This is where the testing happens
    # Teardown code
    # seq_storage.close()

def test_get_name_size(setup_teardown):
   assert len(setup_teardown.get_names()) >= 17

def test_sequence_4_3_A(setup_teardown):
    pseq1 = setup_teardown.pseq['SEQ_4_3_A']
    assert pseq1.get(0) == SEQ_4_3_A[0]
    assert pseq1.get(1) == SEQ_4_3_A[1]
    assert pseq1.get(2) == SEQ_4_3_A[2]
    assert pseq1.get(3) == SEQ_4_3_A[3]

def test_sequence_4_3_B(setup_teardown):
    pseq1 = setup_teardown.pseq['SEQ_4_3_B']
    assert pseq1.get(0) == SEQ_4_3_B[0]
    assert pseq1.get(1) == SEQ_4_3_B[1]
    assert pseq1.get(2) == SEQ_4_3_B[2]
    assert pseq1.get(3) == SEQ_4_3_B[3]

def test_sequence_4_1_A(setup_teardown):
    pseq1 = setup_teardown.pseq['SEQ_4_1_A']
    assert pseq1.get(0) == SEQ_4_1_A[0]
    assert pseq1.get(1) == SEQ_4_1_A[1]
    assert pseq1.get(2) == SEQ_4_1_A[2]
    assert pseq1.get(3) == SEQ_4_1_A[3]


def test_sequence_8_7_A(setup_teardown):
    pseq1 = setup_teardown.pseq['SEQ_8_7_A']
    assert pseq1.get(0) == SEQ_8_7_A[0]
    assert pseq1.get(1) == SEQ_8_7_A[1]
    assert pseq1.get(2) == SEQ_8_7_A[2]
    assert pseq1.get(3) == SEQ_8_7_A[3]

def test_sequence_8_7_B(setup_teardown):
    pseq1 = setup_teardown.pseq['SEQ_8_7_B']
    assert pseq1.get(0) == SEQ_8_7_B[0]
    assert pseq1.get(1) == SEQ_8_7_B[1]
    assert pseq1.get(2) == SEQ_8_7_B[2]
    assert pseq1.get(3) == SEQ_8_7_B[3]


def test_sequence_8_7_C(setup_teardown):
    pseq1 = setup_teardown.pseq['SEQ_8_7_C']
    assert pseq1.get(0) == SEQ_8_7_C[0]
    assert pseq1.get(1) == SEQ_8_7_C[1]
    assert pseq1.get(2) == SEQ_8_7_C[2]
    assert pseq1.get(3) == SEQ_8_7_C[3]

def test_sequence_8_7_D(setup_teardown):
    pseq1 = setup_teardown.pseq['SEQ_8_7_D']
    assert pseq1.get(0) == SEQ_8_7_D[0]
    assert pseq1.get(1) == SEQ_8_7_D[1]
    assert pseq1.get(2) == SEQ_8_7_D[2]
    assert pseq1.get(3) == SEQ_8_7_D[3]

def test_sequence_8_5_A(setup_teardown):
    pseq1 = setup_teardown.pseq['SEQ_8_5_A']
    assert pseq1.get(0) == SEQ_8_5_A[0]
    assert pseq1.get(1) == SEQ_8_5_A[1]
    assert pseq1.get(2) == SEQ_8_5_A[2]

def test_sequence_8_5_B(setup_teardown):
    pseq1 = setup_teardown.pseq['SEQ_8_5_B']
    assert pseq1.get(0) == SEQ_8_5_B[0]
    assert pseq1.get(1) == SEQ_8_5_B[1]
    assert pseq1.get(2) == SEQ_8_5_B[2]

def test_sequence_8_3_A(setup_teardown):
    pseq1 = setup_teardown.pseq['SEQ_8_3_A']
    assert pseq1.get(0) == SEQ_8_3_A[1]
    assert pseq1.get(1) == SEQ_8_3_A[2]
    assert pseq1.get(2) == SEQ_8_3_A[3]


def test_sequence_8_3_B(setup_teardown):
    pseq1 = setup_teardown.pseq['SEQ_8_3_B']
    assert pseq1.get(0) == SEQ_8_3_B[0]
    assert pseq1.get(1) == SEQ_8_3_B[1]
    assert pseq1.get(2) == SEQ_8_3_B[2]


def test_sequence_8_3_C(setup_teardown):
    pseq1 = setup_teardown.pseq['SEQ_8_3_C']
    assert pseq1.get(0) == SEQ_8_3_C[0]
    assert pseq1.get(1) == SEQ_8_3_C[1]
    assert pseq1.get(2) == SEQ_8_3_C[2]


def test_sequence_8_3_D(setup_teardown):
    pseq1 =  setup_teardown.pseq['SEQ_8_3_D']
    assert pseq1.get(0) == SEQ_8_3_D[0]
    assert pseq1.get(1) == SEQ_8_3_D[1]
    assert pseq1.get(2) == SEQ_8_3_D[2]


def test_sequence_8_3_E(setup_teardown):
    pseq1 = setup_teardown.pseq['SEQ_8_3_E']
    assert pseq1.get(0) == SEQ_8_3_E[0]
    assert pseq1.get(1) == SEQ_8_3_E[1]
    assert pseq1.get(2) == SEQ_8_3_E[2]


def test_sequence_8_1_A(setup_teardown):
    pseq1 = setup_teardown.pseq['SEQ_8_1_A']
    assert pseq1.get(0) == SEQ_8_1_A[0]
    assert pseq1.get(1) == SEQ_8_1_A[1]
    assert pseq1.get(2) == SEQ_8_1_A[2]



def test_sequence_8_1_B(setup_teardown):
    pseq1 = setup_teardown.pseq['SEQ_8_1_B']
    assert pseq1.get(0) == SEQ_8_1_B[0]
    assert pseq1.get(1) == SEQ_8_1_B[1]
    assert pseq1.get(2) == SEQ_8_1_B[2]


def test_sequence_6_5_B(setup_teardown):
    pseq1 = setup_teardown.pseq['SEQ_6_5_B']
    assert pseq1.get(0) == SEQ_6_5_B[1]
    assert pseq1.get(1) == SEQ_6_5_B[2]
    assert pseq1.get(2) == SEQ_6_5_B[3]
    assert pseq1.get(3) == SEQ_6_5_B[4]


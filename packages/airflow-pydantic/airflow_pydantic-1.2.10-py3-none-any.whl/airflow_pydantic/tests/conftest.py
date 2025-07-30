from datetime import datetime, timedelta

import pytest
from pytest import fixture

from airflow_pydantic import (
    BashOperator,
    BashOperatorArgs,
    BashSensor,
    BashSensorArgs,
    Dag,
    DagArgs,
    PythonOperator,
    PythonOperatorArgs,
    PythonSensor,
    PythonSensorArgs,
    SSHOperator,
    SSHOperatorArgs,
    TaskArgs,
)

has_balancer = False
try:
    from airflow_balancer import BalancerConfiguration, BalancerHostQueryConfiguration, Host
    from airflow_balancer.testing import pools, variables

    has_balancer = True
except ImportError:
    ...

has_ssh_hook = False
try:
    from airflow.providers.ssh.hooks.ssh import SSHHook

    has_ssh_hook = True
except ImportError:
    ...


def foo(**kwargs): ...


def hook(**kwargs):
    if not has_ssh_hook:
        pytest.skip("SSHHook is not installed, skipping SSHHook fixtures")
        return
    return SSHHook(remote_host="test", username="test")


@fixture
def python_operator_args():
    return PythonOperatorArgs(
        python_callable="airflow_pydantic.tests.conftest.foo",
        op_args=["test"],
        op_kwargs={"test": "test"},
        templates_dict={"test": "test"},
        templates_exts=[".sql", ".hql"],
        show_return_value_in_logs=True,
    )


@fixture
def python_sensor_args():
    return PythonSensorArgs(
        python_callable="airflow_pydantic.tests.conftest.foo",
        op_args=["test"],
        op_kwargs={"test": "test"},
    )


@fixture
def python_operator(python_operator_args):
    return PythonOperator(
        task_id="test_python_operator",
        **python_operator_args.model_dump(),
    )


@fixture
def python_sensor(python_sensor_args):
    return PythonSensor(
        task_id="test_python_sensor",
        **python_sensor_args.model_dump(),
    )


@fixture
def bash_operator_args():
    return BashOperatorArgs(
        bash_command="test",
        env={"test": "test"},
        append_env=True,
        output_encoding="utf-8",
        skip_on_exit_code=99,
        cwd="test",
        output_processor="airflow_pydantic.tests.conftest.foo",
    )


@fixture
def bash_sensor_args():
    return BashSensorArgs(
        bash_command="test",
        cwd="test",
    )


@fixture
def bash_operator(bash_operator_args):
    return BashOperator(
        task_id="test_bash_operator",
        **bash_operator_args.model_dump(),
    )


@fixture
def bash_sensor(bash_sensor_args):
    return BashSensor(
        task_id="test_bash_sensor",
        **bash_sensor_args.model_dump(),
    )


@fixture
def ssh_operator_args():
    if not has_ssh_hook:
        pytest.skip("SSHHook is not installed, skipping SSHHook fixtures")
        return
    return SSHOperatorArgs(
        ssh_conn_id="test",
        ssh_hook="airflow_pydantic.tests.conftest.hook",
        command="test",
        do_xcom_push=True,
        cmd_timeout=10,
        get_pty=True,
        environment={"test": "test"},
    )


@fixture
def ssh_operator(ssh_operator_args):
    if not has_ssh_hook:
        pytest.skip("SSHHook is not installed, skipping SSHHook fixtures")
        return
    return SSHOperator(
        task_id="test_ssh_operator",
        **ssh_operator_args.model_dump(),
    )


@fixture
def balancer():
    if not has_balancer:
        pytest.skip("airflow_balancer is not installed, skipping balancer fixtures")
        return
    with pools():
        return BalancerConfiguration(
            hosts=[
                Host(
                    name="test_host",
                    username="test_user",
                    password_variable="VAR",
                    password_variable_key="password",
                ),
            ]
        )


@fixture
def ssh_operator_balancer(ssh_operator_args, balancer):
    if not has_balancer:
        pytest.skip("airflow_balancer is not installed, skipping balancer fixtures")
    with pools(), variables({"user": "test", "password": "password"}):
        return SSHOperator(
            task_id="test_ssh_operator",
            **ssh_operator_args.model_dump(exclude=["ssh_hook"]),
            ssh_hook=BalancerHostQueryConfiguration(
                kind="select",
                balancer=balancer,
                name="test_host",
            ),
        )


@fixture
def dag_args():
    return DagArgs(
        description="",
        schedule="* * * * *",
        start_date=datetime(2025, 1, 1),
        end_date=datetime(2026, 1, 1),
        max_active_tasks=1,
        max_active_runs=1,
        catchup=False,
        is_paused_upon_creation=True,
        tags=["a", "b"],
        dag_display_name="test",
        enabled=True,
    )


@fixture
def task_args():
    return TaskArgs(
        owner="airflow",
        email=["test@test.com"],
        email_on_failure=True,
        email_on_retry=True,
        retries=3,
        retry_delay=timedelta(minutes=5),
        start_date=datetime(2025, 1, 1),
        end_date=datetime(2026, 1, 1),
        depends_on_past=True,
        queue="default",
        pool="default",
        pool_slots=1,
        do_xcom_push=True,
        task_display_name="test",
    )


@fixture
def dag(dag_args, task_args, python_operator, bash_operator, ssh_operator, bash_sensor, python_sensor):
    return Dag(
        dag_id="a-dag",
        **dag_args.model_dump(),
        default_args=task_args,
        tasks={
            "task1": python_operator,
            "task2": bash_operator,
            "task3": ssh_operator,
            "task4": bash_sensor,
            "task5": python_sensor,
        },
    )


@fixture
def dag_with_external(dag_args, task_args, python_operator, bash_operator, ssh_operator):
    ssh_operator.ssh_hook = hook
    return Dag(
        dag_id="a-dag",
        **dag_args.model_dump(),
        default_args=task_args,
        tasks={
            "task1": python_operator,
            "task2": bash_operator,
            "task3": ssh_operator,
        },
    )

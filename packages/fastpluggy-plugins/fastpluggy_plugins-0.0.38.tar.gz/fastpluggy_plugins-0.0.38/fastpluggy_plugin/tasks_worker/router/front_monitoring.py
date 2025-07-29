from fastapi import Request, Depends, APIRouter
from fastapi.responses import HTMLResponse

from fastpluggy.core.database import get_db
from fastpluggy.core.dependency import get_view_builder
from fastpluggy.core.view_builer.components.button import AutoLinkView
from fastpluggy.core.view_builer.components.table import TableView
from fastpluggy.core.widgets import CustomTemplateWidget
from fastpluggy.core.widgets.categories.data.debug import DebugView
from fastpluggy.core.widgets.categories.input.button_list import ButtonListWidget
from fastpluggy.fastpluggy import FastPluggy

front_monitoring_task_router = APIRouter(
    tags=["task_router"],
)


@front_monitoring_task_router.get("/", response_class=HTMLResponse, name="task_duration_analytics")
async def task_duration_analytics(request: Request, view_builder=Depends(get_view_builder), ):
    items = [
        CustomTemplateWidget(
            template_name='tasks_worker/monitoring/task_time.html.j2',
            context={
                "request": request,
            }
        ),

    ]

    return view_builder.generate(
        request,
        title=f"Task Duration Analytics",
        widgets=items
    )

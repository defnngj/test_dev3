
function SelectInit(defaultProjectId, defaultModuleId) {
    // console.log("初始化Select下拉框");
    console.log("选中的项目", defaultProjectId);
    console.log("选中的模块", defaultModuleId);
    var cmbProject = document.getElementById("selectProject");
    var cmbModule = document.getElementById("selectModule");

    var dataList = [];

    //设置默认选项
    function setDefaultOption(obj, id) {
        console.log("obj", obj.options.length);
        console.log("============id=============?", id);
        for (var i = 0; i < obj.options.length; i++) {
            if (obj.options[i].value == id) {
                obj.selectedIndex = i;
                return;
            }
        }
    }
    //创建下拉选项
    function addOption(cmb, obj) {
        var option = document.createElement("option");
        cmb.options.add(option);
        option.innerHTML = obj.name;
        option.value = obj.id;
        console.log("option", option);
    }

    //改变项目
    function changeProject() {
        cmbModule.options.length = 0;
        // console.log("项目默认选项的索引", cmbProject.selectedIndex);
        var pid = cmbProject.options[cmbProject.selectedIndex].value;
        // console.log("这个才是真的项目id", pid);

        for (var i = 0; i < dataList.length; i++) {
            if (dataList[i].id == pid) {
                var modules = dataList[i].moduleList;
                // console.log("对应的模块列表", modules);
                for (var j = 0; j < modules.length; j++) {
                    addOption(cmbModule, modules[j]);
                }
            }
        }
        setDefaultOption(cmbModule, defaultModuleId);
    }

    function getSelectData() {
        // 调用获取select数据列表
        $.get("/case/get_select_data/", {}, function (resp) {
            if (resp.code === 10200) {
                dataList = resp.data;
                //console.log("想要的数据格式-->", dataList);
                //遍历项目
                for (var i = 0; i < dataList.length; i++) {
                    //console.log("每一个项目的数据", dataList[i]);
                    addOption(cmbProject, dataList[i]);
                }

                setDefaultOption(cmbProject, defaultProjectId);
                changeProject();
                cmbProject.onchange = changeProject;
            }
            setDefaultOption(cmbProject, defaultProjectId);

        });
    }

    getSelectData();
}

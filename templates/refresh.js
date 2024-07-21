window.onload = function() {
  var refreshContainer = document.getElementById('refresh-container');
  var refreshContent = document.getElementById('refresh-content');
  var refreshLink = document.createElement('a');
  refreshLink.href = '/get_data'; // 替换为您的链接地址

  refreshContainer.addEventListener('touchstart', touchStart, false);
  refreshContainer.addEventListener('touchmove', touchMove, false);
  refreshContainer.addEventListener('touchend', touchEnd, false);

  function touchStart(e) {
    // 记录初始触摸位置和距离
    var touchY = e.touches[0].pageY;
    // 添加点击事件，用于获取数据
    refreshLink.addEventListener('click', fetchData, false);
    // 添加 touchend 事件，用于取消点击状态
    e.target.addEventListener('touchend', removeLinkListener, false);
  }

  function touchMove(e) {
    // 计算当前距离和移动距离，如果移动距离大于刷新高度，则进入刷新状态，否则取消刷新状态
    var currentDistance = e.touches[0].pageY;
    if (Math.abs(currentDistance - touchY) >= refreshHeight) {
      if (currentDistance > touchY) { // 下滑刷新操作
        if (!refreshActive) { // 如果不是正在刷新状态，则进入刷新状态并显示刷新文本
          refreshActive = true;
          refreshContent.innerHTML = '下拉刷新...';
        }
      } else { // 上滑操作，不做处理，直接取消刷新状态即可
        refreshActive = false;
        clearTimeout(refreshTimeout); // 清除定时器，避免重复触发刷新操作
      }
    } else { // 移动距离小于刷新高度，取消刷新状态并显示原有内容
      if (refreshActive) { // 如果处于刷新状态，则取消刷新状态并显示原有内容
        refreshActive = false;
        clearTimeout(refreshTimeout); // 清除定时器，避免重复触发刷新操作
        refreshContent.innerHTML = ''; // 清空内容，显示原有内容
      } else { // 如果不是处于刷新状态，则不做处理，保持原有状态不变
        return;
      }
    }
  }

  function touchEnd(e) { // 结束触摸操作，自动触发刷新操作或取消刷新操作（根据移动距离判断）
    if (Math.abs(e.changedTouches[0].pageY - touchY) >= refreshHeight) { // 移动距离大于刷新高度，自动触发刷新操作（模拟下拉刷新的效果）
      if (!refreshActive) { // 如果不是正在刷新状态，则进入刷新状态并显示刷新文本，同时设置定时器延迟执行刷新操作（模拟加载动画的效果）
        refreshActive = true;
        refreshContent.innerHTML = '正在加载...'; // 显示刷新文本（模拟下拉刷新的效果）
        // 使用 fetch() 发送请求并获取数据
        fetch(refreshLink.href)
          .then(function(response) {
            // 处理响应数据，例如解析 JSON 数据等操作
            return response.json();
          })
          .then(function(data) {
            // 处理获取到的数据，例如更新页面内容等操作
            // 这里根据您的需求进行相应的处理操作
          })
          .catch(function(error) {
            // 处理请求错误情况的操作
            console.error('Error:', error);
          });
        // 设置定时器延迟执行刷新操作（模拟加载动画的效果）
        refreshTimeout = setTimeout(refreshContent, 2000); // 设置定时器延迟2秒执行刷新操作
      } else { // 如果处于刷新状态，则取消刷新状态并显示原有内容
        refreshActive = false;
        clearTimeout(refreshTimeout); // 清除定时器，避免重复触发刷新操作
        refreshContent.innerHTML = ''; // 清空内容，显示原有内容
      }
    } else { // 如果移动距离小于刷新高度，取消刷新状态并显示原有内容
      if (refreshActive) { // 如果处于刷新状态，则取消刷新状态并显示原有内容
        refreshActive = false;
        clearTimeout(refreshTimeout); // 清除定时器，避免重复触发刷新操作
        refreshContent.innerHTML = ''; // 清空内容，显示原有
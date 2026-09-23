package jp.ac.jec.a04funnycamera

import android.content.Context
import android.util.AttributeSet
import android.view.MotionEvent
import android.view.View
import androidx.appcompat.widget.AppCompatImageView

/**
 * 指でドラッグして移動できるImageView
 *
 * 親Viewの内側からはみ出さない範囲で移動する
 */
class DraggableImageView @JvmOverloads constructor(
    context: Context,
    attrs: AttributeSet? = null,
    defStyleAttr: Int = 0
) : AppCompatImageView(context, attrs, defStyleAttr) {

    // タッチした位置とこのViewの左上の差分
    private var offsetX = 0f
    private var offsetY = 0f

    override fun onTouchEvent(event: MotionEvent): Boolean {
        when (event.actionMasked) {
            MotionEvent.ACTION_DOWN -> {
                offsetX = x - event.rawX
                offsetY = y - event.rawY
            }

            MotionEvent.ACTION_MOVE -> {
                moveTo(event.rawX + offsetX, event.rawY + offsetY)
            }

            MotionEvent.ACTION_UP -> performClick() // （アクセシビリティ対応）
        }
        return true
    }

    override fun performClick(): Boolean {
        return super.performClick()
    }

    /**
     * 指定した位置に移動する (親Viewの内側からはみ出さないように位置を補正する)
     */
    private fun moveTo(newX: Float, newY: Float) {
        val parentView = parent as? View ?: return
        // 親Viewのpaddingを除いた範囲の左上と右下
        val minX = parentView.paddingLeft.toFloat()
        val minY = parentView.paddingTop.toFloat()
        val maxX = (parentView.width - parentView.paddingRight - width).toFloat()
        val maxY = (parentView.height - parentView.paddingBottom - height).toFloat()

        x = newX.coerceAtMost(maxX).coerceAtLeast(minX)
        y = newY.coerceAtMost(maxY).coerceAtLeast(minY)
    }
}

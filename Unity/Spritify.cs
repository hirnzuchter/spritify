using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[ExecuteInEditMode]
public class Spritify : MonoBehaviour
{

    public Material EffectMaterial;

    void OnRenderImage(RenderTexture dst, RenderTexture src)
    {
        Graphics.Blit(src, dst, EffectMaterial);
    }
}
